"""Generate only explicitly synthetic fixtures; no research/network/model calls."""
import json
from pathlib import Path
from cloud_pilot.contract import envelope

ALPHA = [
'''The fictional Aurora Parcel EV is a training example for comparing a seller's vehicle description with a bounded specification sheet. Its invented identity is Aurora, model year 2026, generation A, Parcel trim, battery electric powertrain, and the fictional Alpha market. These labels belong together. A description of another trim does not establish the equipment supplied with this example. A buyer in this imagined exercise can decide whether the identity record is sufficiently precise to request a matching document set.''',
'''The synthetic Alpha specification sheet assigns the Parcel trim a battery capacity of 42 kWh. That number describes only this made-up trim and market. It says nothing about usable energy, degradation, replacement cost, or a vehicle offered by a real seller. The example asks the reader to retain the unit beside the number and to distinguish the capacity label from a promise about driving distance. No physical battery was inspected to produce this illustration.''',
'''The equally fictional range certificate states 280 km under the invented SIM-A test cycle. SIM-A is a label created for this exercise; it is not CLTC, WLTP, NEDC, or EPA. The range should therefore remain attached to its own label when the document is summarized. Converting the figure into an expected delivery route length would introduce an unsupported assumption. The certificate does not address cold weather, load, road gradient, or charging stops.''',
'''In the imaginary equipment annex, the Parcel trim has two seats and a separated cargo compartment. Those entries support a discussion of seating and compartment layout within the example. They do not establish payload, gross weight, towing capability, or cargo dimensions. A procurement comparison that depends on any of those missing figures remains incomplete. The buyer's next action in this training scenario is to request the relevant measurements and matching identity documents, rather than infer capacity from a photograph.''',
'''The invented connector appendix labels the charging inlet Type-SIM. The label has no claimed equivalence with any connector sold in a real market. A destination charger cannot be assumed compatible merely because its socket looks similar in an illustration. The example separates a connector identity from charging performance: no charging curve, peak power, charging time, electrical approval, or adapter permission is provided. Each of those questions would require its own applicable evidence before a commercial decision.''',
'''The fictional buyer record leaves price, availability, freight, import eligibility, warranty coverage, and after-sales arrangements unresolved. There is no offer or contract behind this text. Within the example, the useful result is a precise list of known identity fields and unanswered transaction questions. It is not a recommendation to buy, a claim that a vehicle can be registered, or a statement that a seller has stock. All organizations and source addresses attached to this example are synthetic and must not be reused as commercial references.'''
]
BETA = [
'''The invented Boreal Shuttle Hybrid concerns a different purchasing question: how to distinguish two passenger-layout documents without borrowing specifications from another vehicle. This example fixes model year 2026, generation B, Shuttle trim, a hybrid powertrain, and the imaginary Beta market. Boreal is not asserted to be a real brand. A reader can use the example to recognize which document belongs to the stated variant and which questions remain outside the supplied evidence.''',
'''The synthetic cabin schedule describes six seats for this particular Shuttle configuration. It does not establish how much luggage fits with every seat occupied. Nor does the seating entry prove accessibility features, child-restraint provisions, passenger-service licensing, or crash performance. Those are separate questions. In this fictional comparison, the purchasing team retains the seat count as a bounded statement and leaves operational suitability open until the missing layout and destination requirements have been examined.''',
'''An imaginary driveline note identifies the example as a hybrid, with the designation HYB-SIM. It deliberately contains no engine displacement, motor output, torque rating, fuel-consumption result, or battery-energy number. The buyer cannot fill those gaps by finding a superficially similar vehicle elsewhere. A shared body shape would not prove shared components. This paragraph illustrates why a powertrain label and a complete technical specification should be recorded as different levels of information.''',
'''The fabricated service note says that a component catalogue is supplied as document CAT-B for the Shuttle trim. It does not promise parts inventory, delivery time, repair capacity, diagnostic access, or service coverage in another country. Possessing a catalogue and having a functioning support arrangement are different things. In the imaginary procurement file, the catalogue is useful for identifying requested parts; it is not evidence that any real business has agreed to supply or install them.''',
'''The fictional body drawing names a left-side sliding passenger door. That description belongs only to the pictured configuration in the invented Beta record. No right-side door, power operation, safety sensor, opening dimension, or conversion approval is stated. The illustration is not a photograph of an AutoBridge inspection. A buyer reviewing this example can mark the door-side requirement as documented while keeping passenger access, destination rules, and exact dimensions on the unanswered list.''',
'''The synthetic comparison ends with a deliberately limited decision: the supplied identity and layout records can be organized into a request for clarification. They cannot support a quotation, import recommendation, warranty promise, or claim about commercial passenger service. No price or legal rule has been researched for this example. The six source records are invented teaching materials, their addresses are nonresolving reserved domains, and their publisher names do not identify actual authorities. This boundary remains part of the example wherever the text is copied.'''
]

def make(aid, title, paragraphs, market, trim, generation, powertrain, cycle):
    p = envelope(aid)
    p.update(title=title, topic_key=aid.lower(), proposed_url='/mock-only/'+aid.lower()+'/',
             search_intent='Synthetic comparison task for '+aid, buyer_task=title,
             research_status='RESEARCH_PASS', research_lock=False, writing_ai_ready=True,
             allowed_facts=[], blocked_facts=['commercial_terms','destination_eligibility'],
             facts=[], sources=[], fixture_type='SHORT_FORM_CONTRACT_TEST_NOT_PUBLISH_GRADE')
    scope=dict(market=market,model_year='2026',generation=generation,trim=trim,powertrain=powertrain,test_cycle=cycle)
    for i, paragraph in enumerate(paragraphs):
        fid,sid=f'F{i+1}',f'S{i+1}'
        p['allowed_facts'].append(fid)
        p['facts'].append(dict(id=fid,text=paragraph,confidence='VERIFIED',source_ids=[sid],**scope))
        org=f'Synthetic Organization {i%4+1}'
        p['sources'].append(dict(id=sid,title=f'Synthetic document {i+1}',publisher=org,observed_publisher=org,
             parent_org=org,url=f'https://synthetic-{i%4+1}.invalid/{aid}/document-{i+1}',tier='T1',
             official_source=True,scope_match='MATCHED',synthetic=True,access_status='FIXTURE_ONLY',
             checked_date='2026-11-02',supported_facts=[fid],excerpt=paragraph,**scope))
    return p

if __name__ == '__main__':
    folder=Path(__file__).parent
    specs=[('MOCK-AURORA','Aurora Parcel EV: a fictional specification comparison',ALPHA,'MOCK-ALPHA','Parcel','A','BEV','SIM-A'),
           ('MOCK-BOREAL','Boreal Shuttle Hybrid: a fictional passenger-layout review',BETA,'MOCK-BETA','Shuttle','B','HYBRID','N/A')]
    for spec in specs:
        packet=make(*spec)
        (folder/(spec[0]+'.json')).write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
