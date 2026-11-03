import base64
import copy
import hashlib
import json
import unittest
from datetime import datetime,timezone
from cloud_pilot.contract import digest,GateError
from cloud_pilot.multilingual.sources import extract
from cloud_pilot.multilingual.source_cache import restore,validate,archive_content_type
from cloud_pilot.multilingual.startup import EpochJournal
from cloud_pilot.multilingual.tests.test_multilingual import ArtifactStore
from cloud_pilot.multilingual.accounting import ResponseJournal
from cloud_pilot.stage2_tests.test_live import plan

class Tests(unittest.TestCase):
    def test_literal_inline_spec_is_selected_without_decoding_or_executing_scripts(self):
        source=dict(url='https://car.autohome.com.cn/config/spec/74130.html')
        config=dict(result=dict(specid=74130,paramtypeitems=[dict(paramitems=[
            dict(name='能源类型',valueitems=[dict(specid=74130,value='纯电动'),dict(specid=1,value='WRONG VEHICLE')]),
            dict(name='电池能量(kWh)',valueitems=[dict(specid=74130,value='51.9')]),
            dict(name='<span>masked label</span>',valueitems=[dict(specid=74130,value='must not infer')])])]))
        raw=('<html><p>'+('public page context '*20)+'</p><script>var config = '+json.dumps(config)+'; throw new Error("MUST NEVER EXECUTE");</script></html>').encode()
        text=extract(raw,'text/html;charset=utf-8',source)
        self.assertIn('能源类型: 纯电动',text);self.assertIn('电池能量(kWh): 51.9',text)
        self.assertNotIn('WRONG VEHICLE',text);self.assertNotIn('must not infer',text)

    def transfer_fixture(self):
        topic=plan()['articles'][0];topic['content_type']='BUYING_GUIDE';old=[];blobs={}
        for i,s in enumerate(topic['sources']):
            raw=('<p>'+('synthetic public evidence '+str(i)+'; ')*20+'</p>').encode()
            sha=hashlib.sha256(raw).hexdigest();blob='blob-'+str(i);path='cloud_pilot/live_artifacts/sources/'+sha+'.bin'
            e=dict(source_id=s['source_id'],requested_url=s['url'],final_url=s['url'],
                publisher=s['publisher'],parent_org=s['parent_org'],tier=s['tier'],scope=s['scope'],
                mime='text/html',retrieved_at=datetime.now(timezone.utc).isoformat(),raw_sha256=sha,
                raw_artifact_path=path,raw_artifact_blob=blob,text=extract(raw,'text/html',s))
            e['text_sha256']=hashlib.sha256(e['text'].encode()).hexdigest()
            old.append(e);blobs[path]=(blob,raw)
        class API:
            tamper=False
            def request(api,method,path):
                entry=next(v for k,v in blobs.items() if k in path)
                raw=entry[1]+(b'changed' if api.tamper else b'')
                return 200,dict(sha=entry[0],encoding='base64',content=base64.b64encode(raw).decode())
        class GH:prefix='/repos/synthetic/repo';api=API()
        j=ResponseJournal(ArtifactStore());j.checkpoint('origin',old);scoped=EpochJournal(j,1,{'code':'new'})
        permit=dict(source_evidence_transfers=[dict(article_id=topic['article_id'],origin_checkpoint='origin',origin_evidence_hash=digest(old),operator_verified=True)])
        return topic,old,j,scoped,GH(),permit

    def test_protected_transfer_checks_raw_hash_and_preserves_dates_and_declarations(self):
        topic,old,j,scoped,gh,p=self.transfer_fixture()
        proof=restore(p,dict(articles=[topic]),j,scoped,gh,'new-code')
        actual=scoped.get_checkpoint('evidence:'+topic['article_id']);validate(actual,topic)
        self.assertEqual([e['retrieved_at'] for e in old],proof[0]['original_retrieval_times'])
        self.assertEqual(proof,restore(p,dict(articles=[topic]),j,scoped,gh,'new-code'))
        changed=copy.deepcopy(actual);changed[0]['scope']['trim']='another trim'
        changed[0]['evidence_hash']=digest({k:v for k,v in changed[0].items() if k!='evidence_hash'})
        with self.assertRaisesRegex(GateError,'DECLARATION_DRIFT'):validate(changed,topic)

    def test_changed_raw_archive_blocks_transfer_before_any_research(self):
        topic,old,j,scoped,gh,p=self.transfer_fixture();gh.api.tamper=True
        with self.assertRaisesRegex(GateError,'RAW_CONTENT'):restore(p,dict(articles=[topic]),j,scoped,gh,'new-code')
        self.assertIsNone(scoped.get_checkpoint('evidence:'+topic['article_id']))

    def test_archive_charset_requires_exact_original_text_not_conflicting_meta(self):
        raw=('<meta charset="gb2312"><p>'+('公开车型参数测试 '*30)+'</p>').encode()
        text=extract(raw,'text/html;charset=utf-8',dict(url='https://example.invalid/'))
        e=dict(mime='text/html',text=text,text_sha256=hashlib.sha256(text.encode()).hexdigest())
        self.assertEqual(archive_content_type(raw,e),'text/html;charset=utf-8')
        e['text']='invented text';e['text_sha256']=hashlib.sha256(e['text'].encode()).hexdigest()
        with self.assertRaisesRegex(GateError,'CHARSET_UNPROVEN'):archive_content_type(raw,e)

if __name__=='__main__':unittest.main()
