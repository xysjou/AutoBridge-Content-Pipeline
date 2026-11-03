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
            raw=('<title>Synthetic source '+str(i)+'</title><p>'+('synthetic public evidence '+str(i)+'; ')*20+'</p>').encode()
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
                entry=next(v for k,v in blobs.items() if k in path or path.endswith('/git/blobs/'+v[0]))
                raw=entry[1]+(b'changed' if api.tamper else b'')
                return 200,dict(sha=entry[0],encoding='base64',content=base64.b64encode(raw).decode())
        class GH:prefix='/repos/synthetic/repo';api=API()
        j=ResponseJournal(ArtifactStore());j.checkpoint('origin',old);scoped=EpochJournal(j,1,{'code':'new'})
        permit=dict(source_evidence_transfers=[dict(article_id=topic['article_id'],origin_checkpoint='origin',origin_evidence_hash=digest(old),operator_verified=True)])
        out=[]
        for i,e in enumerate(old):
            new=copy.deepcopy(e);new.update(content_type='text/html;charset=utf-8',source_title='Synthetic source '+str(i),representation_code_sha='new-code',archive_origin_checkpoint='origin')
            new['evidence_hash']=digest(new);out.append(new)
        permit['source_evidence_transfers'][0].update(expected_target_checkpoint=scoped.prefix+'evidence:'+topic['article_id'],expected_target_evidence_hash=digest(out))
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
        with self.assertRaisesRegex(GateError,'RAW_CONTENT') as caught:restore(p,dict(articles=[topic]),j,scoped,gh,'new-code')
        self.assertEqual(topic['article_id'],caught.exception.article_id)
        self.assertEqual(topic['sources'][0]['source_id'],caught.exception.source['source_id'])
        self.assertEqual(topic['sources'][0]['url'],caught.exception.source['url'])
        self.assertIsNone(scoped.get_checkpoint('evidence:'+topic['article_id']))

    def test_cached_transfer_cannot_claim_an_unrelated_origin(self):
        topic,old,j,scoped,gh,p=self.transfer_fixture()
        restore(p,dict(articles=[topic]),j,scoped,gh,'new-code')
        different=copy.deepcopy(old);different[0]['raw_sha256']='a'*64
        j.checkpoint('another-origin',different)
        d=p['source_evidence_transfers'][0];d.update(origin_checkpoint='another-origin',origin_evidence_hash=digest(different))
        with self.assertRaisesRegex(GateError,'RAW_|CACHED_ORIGIN_DRIFT|PROOF_DRIFT|EXPECTED_TARGET_DRIFT'):
            restore(p,dict(articles=[topic]),j,scoped,gh,'new-code')

    def test_self_consistent_forged_cached_text_is_reconstructed_from_raw(self):
        topic,old,j,scoped,gh,p=self.transfer_fixture()
        restore(p,dict(articles=[topic]),j,scoped,gh,'new-code')
        cached=scoped.get_checkpoint('evidence:'+topic['article_id']);cached[0]['text']='forged text'
        cached[0]['text_sha256']=hashlib.sha256(b'forged text').hexdigest()
        cached[0]['evidence_hash']=digest({k:v for k,v in cached[0].items() if k!='evidence_hash'})
        real_get=scoped.get_checkpoint
        scoped.get_checkpoint=lambda key:cached if key=='evidence:'+topic['article_id'] else real_get(key)
        with self.assertRaisesRegex(GateError,'RECONSTRUCTED_TARGET_DRIFT'):
            restore(p,dict(articles=[topic]),j,scoped,gh,'new-code')

    def test_archive_charset_requires_exact_original_text_not_conflicting_meta(self):
        raw=('<meta charset="gb2312"><p>'+('公开车型参数测试 '*30)+'</p>').encode()
        text=extract(raw,'text/html;charset=utf-8',dict(url='https://example.invalid/'))
        e=dict(mime='text/html',text=text,text_sha256=hashlib.sha256(text.encode()).hexdigest())
        self.assertEqual(archive_content_type(raw,e),'text/html;charset=utf-8')
        e['text']='invented text';e['text_sha256']=hashlib.sha256(e['text'].encode()).hexdigest()
        with self.assertRaisesRegex(GateError,'CHARSET_UNPROVEN'):archive_content_type(raw,e)

    def test_existing_non_utf8_archive_uses_binary_git_blob(self):
        from cloud_pilot.live.http import GitHubTransport
        from cloud_pilot.live.policy import BRANCH
        raw=('原始网页中文正文'*20).encode('gb18030')
        class API:
            host='api.github.com'
            def request(self,method,path,payload=None):
                data=raw if '/git/blobs/' in path else b'contents representation'
                return 200,dict(sha='original-blob',encoding='base64',content=base64.b64encode(data).decode())
        transport=GitHubTransport(API())
        self.assertEqual(transport.put_immutable(BRANCH,'cloud_pilot/live_artifacts/sources/example.bin',raw),'original-blob')
        with self.assertRaisesRegex(GateError,'IMMUTABLE_ARTIFACT_CONFLICT'):
            transport.put_immutable(BRANCH,'cloud_pilot/live_artifacts/sources/example.bin',raw+b'changed')

if __name__=='__main__':unittest.main()
