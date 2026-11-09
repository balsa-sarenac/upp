"""Generate conceptual class 3 examples; run from any working directory."""
from pathlib import Path
import json
import xml.etree.ElementTree as E

OUT = Path(__file__).resolve().parents[2] / '2026-2027/vjezbe/class3/bpmn-class3'
NS = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
      'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
      'dc': 'http://www.omg.org/spec/DD/20100524/DC',
      'di': 'http://www.omg.org/spec/DD/20100524/DI'}
for prefix, uri in NS.items():
    E.register_namespace(prefix, uri)


def el(parent, tag, **attrs):
    prefix, local = tag.split(':')
    return E.SubElement(parent, '{' + NS[prefix] + '}' + local,
                        {k: str(v) for k, v in attrs.items()})


class Draft:
    def __init__(self, name, title, collaboration=False):
        self.name, self.title = name, title
        self.root = E.Element('{' + NS['bpmn'] + '}definitions',
                              id='Definitions', targetNamespace='https://upp.example/class3')
        self.process = el(self.root, 'bpmn:process', id='Process', isExecutable='false')
        diagram = el(self.root, 'bpmndi:BPMNDiagram', id='Diagram')
        self.plane = el(diagram, 'bpmndi:BPMNPlane', id='Plane',
                        bpmnElement='Collaboration' if collaboration else 'Process')
        self.nodes = {}
        self.serial = 0

    def node(self, id, kind, name, x, y, parent=None, w=None, h=None, **attrs):
        w = w or (50 if 'Gateway' in kind else 36 if 'Event' in kind else 160)
        h = h or (50 if 'Gateway' in kind else 36 if 'Event' in kind else 80)
        obj = el(self.process if parent is None else parent, 'bpmn:' + kind,
                 id=id, name=name, **attrs)
        self.nodes[id] = (obj, x, y, w, h)
        shape = el(self.plane, 'bpmndi:BPMNShape', id=id + '_di', bpmnElement=id)
        if kind == 'participant': shape.set('isHorizontal', 'true')
        if kind == 'subProcess': shape.set('isExpanded', 'true')
        if kind == 'exclusiveGateway': shape.set('isMarkerVisible', 'true')
        el(shape, 'dc:Bounds', x=x, y=y, width=w, height=h)
        if 'Event' in kind or 'Gateway' in kind or kind in ('dataObjectReference', 'dataStoreReference'):
            label = el(shape, 'bpmndi:BPMNLabel')
            # Gateway labels sit above-left, clear of the up and down branches.
            el(label, 'dc:Bounds', x=x-125 if 'Gateway' in kind else x-60,
               y=y-35 if 'Gateway' in kind else y+h+8, width=120 if 'Gateway' in kind else 160, height=30 if 'Gateway' in kind else 55)
        return obj

    def flow(self, a, b, name='', points=None, message=False, parent=None, label_at=None):
        self.serial += 1
        id = 'Flow_' + str(self.serial)
        A, x, y, w, h = self.nodes[a]
        B, bx, by, bw, bh = self.nodes[b]
        obj = el(self.process if parent is None else parent,
                 'bpmn:messageFlow' if message else 'bpmn:sequenceFlow',
                 id=id, sourceRef=a, targetRef=b, name=name)
        if not message:
            el(A, 'bpmn:outgoing').text = id
            el(B, 'bpmn:incoming').text = id
        edge = el(self.plane, 'bpmndi:BPMNEdge', id=id+'_di', bpmnElement=id)
        points = points or [(x+w, y+h/2), (bx, by+bh/2)]
        for px, py in points: el(edge, 'di:waypoint', x=px, y=py)
        if name:
            label = el(edge, 'bpmndi:BPMNLabel')
            (x1,y1),(x2,y2)=max(zip(points,points[1:]),key=lambda s:abs(s[1][0]-s[0][0])+abs(s[1][1]-s[0][1]))
            px,py=label_at or ((x1+x2)/2+10 if x1==x2 else (x1+x2)/2-65,
                              (y1+y2)/2-30)
            el(label, 'dc:Bounds', x=px, y=py, width=130, height=44)
        return obj

    def event(self, obj, kind, **attrs):
        return el(obj, 'bpmn:' + kind + 'EventDefinition', **attrs)

    def save(self):
        ids = [n.get('id') for n in self.root.iter() if n.get('id')]
        assert len(ids) == len(set(ids)), self.name
        for obj in self.root.iter():
            for key in ('sourceRef', 'targetRef', 'attachedToRef', 'processRef'):
                if obj.get(key): assert obj.get(key) in ids, (self.name, key, obj.get(key))
        E.indent(self.root)
        E.ElementTree(self.root).write(OUT / (self.name+'.bpmn'), encoding='utf-8', xml_declaration=True)
        manifest.append({'name': self.name, 'title': self.title, 'fontSize': 16})


def pool(m, name, lanes, w=1000):
    """Draw one pool with lanes stacked from y=20; return {lane name: lane element}."""
    collab = el(m.root, 'bpmn:collaboration', id='Collaboration')
    m.node('Pool', 'participant', name, 20, 20, parent=collab, w=w, h=sum(h for _, h in lanes), processRef='Process')
    lane_set = el(m.process, 'bpmn:laneSet', id='LaneSet')
    result, y = {}, 20
    for i, (lane_name, h) in enumerate(lanes):
        lane = el(lane_set, 'bpmn:lane', id=f'Lane{i}', name=lane_name)
        shape = el(m.plane, 'bpmndi:BPMNShape', id=f'Lane{i}_di', bpmnElement=f'Lane{i}', isHorizontal='true')
        el(shape, 'dc:Bounds', x=50, y=y, width=w-30, height=h)
        result[lane_name], y = lane, y + h
    return result


def assign(lane, *ids):
    for id in ids: el(lane, 'bpmn:flowNodeRef').text = id


OUT.mkdir(parents=True, exist_ok=True)
manifest = []
# Minimal examples introduce each new element before the task that uses it.
m = Draft('01-message-basics', 'Упит за цијену: оба процеса', True)
collab = el(m.root, 'bpmn:collaboration', id='Collaboration')
shop = el(m.root, 'bpmn:process', id='ShopProcess', isExecutable='false')
el(m.root, 'bpmn:message', id='QueryMessage', name='Упит + број')
el(m.root, 'bpmn:message', id='PriceMessage', name='Цијена + број упита')
m.node('Buyer', 'participant', 'Купац', 20, 20, parent=collab, w=900, h=180, processRef='Process')
m.node('Shop', 'participant', 'Продавница', 20, 320, parent=collab, w=900, h=180, processRef='ShopProcess')
m.node('Start', 'startEvent', '', 80, 92)
m.node('Send', 'sendTask', 'Послати упит', 170, 70, messageRef='QueryMessage')
m.node('Receive', 'receiveTask', 'Примити цијену', 560, 70, messageRef='PriceMessage')
m.node('End', 'endEvent', '', 820, 92)
st = m.node('ShopStart', 'startEvent', 'Упит примљен', 232, 392, parent=shop)
m.event(st, 'message', messageRef='QueryMessage')
m.node('Calc', 'task', 'Израчунати цијену', 330, 370, parent=shop)
m.node('Reply', 'sendTask', 'Послати цијену', 560, 370, parent=shop, messageRef='PriceMessage')
m.node('ShopEnd', 'endEvent', '', 820, 392, parent=shop)
m.flow('Start', 'Send'); m.flow('Send', 'Receive'); m.flow('Receive', 'End')
m.flow('ShopStart', 'Calc', parent=shop); m.flow('Calc', 'Reply', parent=shop); m.flow('Reply', 'ShopEnd', parent=shop)
m.flow('Send', 'ShopStart', 'упит бр. 17', [(250, 150), (250, 392)], message=True, parent=collab, label_at=(260, 240))
m.flow('Reply', 'Receive', 'цијена, бр. 17', [(640, 370), (640, 150)], message=True, parent=collab, label_at=(650, 240))
m.save()

# Two fully modelled participants, linked by order and reply messages.
m = Draft('02-messages', 'Слање наруџбине и пријем одговора', True)
collab = el(m.root, 'bpmn:collaboration', id='Collaboration')
supplier = el(m.root, 'bpmn:process', id='SupplierProcess', isExecutable='false')
el(m.root, 'bpmn:message', id='OrderMessage', name='Наруџбина + ID')
el(m.root, 'bpmn:message', id='ReplyMessage', name='Одговор + ID')
m.node('Buyer', 'participant', 'Набавка', 20, 20, parent=collab, w=1200, h=300, processRef='Process')
m.node('Supplier', 'participant', 'Добављач', 20, 430, parent=collab, w=1200, h=200, processRef='SupplierProcess')
m.node('Start', 'startEvent', '', 80, 102)
m.node('Send', 'sendTask', 'Послати наруџбину', 180, 80, messageRef='OrderMessage')
m.node('Receive', 'receiveTask', 'Примити одговор', 500, 80, messageRef='ReplyMessage')
t = m.node('Timeout', 'boundaryEvent', 'Два дана', 610, 142, attachedToRef='Receive', cancelActivity='true')
el(m.event(t, 'timer'), 'bpmn:timeDuration').text = 'P2D'
m.node('Decision', 'exclusiveGateway', 'Прихваћено?', 770, 95)
m.node('Accepted', 'endEvent', 'Прихваћено', 1080, 50)
m.node('Rejected', 'endEvent', 'Одбијено', 1080, 150)
m.node('Notify', 'serviceTask', 'Обавијестити: нема одговора', 730, 220, w=220)
m.node('Expired', 'endEvent', '', 1080, 242)
s = m.node('SupplierStart', 'startEvent', 'Наруџбина', 242, 482, parent=supplier)
m.event(s, 'message', messageRef='OrderMessage')
m.node('Handle', 'task', 'Обрадити наруџбину', 330, 460, parent=supplier)
m.node('Reply', 'sendTask', 'Послати одговор', 520, 460, parent=supplier, messageRef='ReplyMessage')
m.node('SupplierEnd', 'endEvent', '', 900, 482, parent=supplier)
m.flow('Start', 'Send'); m.flow('Send', 'Receive'); m.flow('Receive', 'Decision')
m.flow('Decision', 'Accepted', 'да', [(795,95),(795,68),(1080,68)])
m.flow('Decision', 'Rejected', 'не', [(820,120),(1000,120),(1000,168),(1080,168)])
m.flow('Timeout','Notify',points=[(628,178),(628,260),(730,260)])
m.flow('Notify','Expired')
m.flow('SupplierStart','Handle',parent=supplier); m.flow('Handle','Reply',parent=supplier); m.flow('Reply','SupplierEnd',parent=supplier)
m.flow('Send','SupplierStart','наруџбина + ID',[(260,160),(260,482)],message=True,parent=collab,label_at=(270,350))
m.flow('Reply','Receive','одговор + ID',[(560,460),(560,160)],message=True,parent=collab,label_at=(570,350))
m.save()

m = Draft('04-event-choice', 'Потврда, одбијање или истек рока')
el(m.root, 'bpmn:message', id='ConfirmMessage', name='Потврда + број наруџбине')
el(m.root, 'bpmn:message', id='RejectMessage', name='Одбијање + број наруџбине')
m.node('Start','startEvent','',40,182)
m.node('Send','sendTask','Послати наруџбину',140,160)
m.node('Wait','eventBasedGateway','Шта стиже прво?',390,175)
c=m.node('Confirm','intermediateCatchEvent','Потврда',570,60);m.event(c,'message',messageRef='ConfirmMessage')
r=m.node('Reject','intermediateCatchEvent','Одбијање',570,182);m.event(r,'message',messageRef='RejectMessage')
t=m.node('Timer','intermediateCatchEvent','Два дана',570,300);el(m.event(t,'timer'),'bpmn:timeDuration').text='P2D'
m.node('Yes','endEvent','Прихваћено',1000,60);m.node('No','endEvent','Одбијено',1000,182)
m.node('Notify','serviceTask','Обавијестити: нема одговора',700,278,w=220);m.node('End','endEvent','',1000,300)
m.flow('Start','Send');m.flow('Send','Wait')
m.flow('Wait','Confirm',points=[(415,175),(415,78),(570,78)])
m.flow('Wait','Reject')
m.flow('Wait','Timer',points=[(415,225),(415,318),(570,318)])
m.flow('Confirm','Yes');m.flow('Reject','No');m.flow('Timer','Notify');m.flow('Notify','End');m.save()

m=Draft('03-event-basics','Event-based gateway: први догађај бира путању')
el(m.root,'bpmn:message',id='AnyMessage',name='Порука')
m.node('Start','startEvent','',40,132);m.node('Wait','eventBasedGateway','Шта стиже прво?',140,125)
r=m.node('Msg','intermediateCatchEvent','Порука',300,40);m.event(r,'message',messageRef='AnyMessage')
t=m.node('Timer','intermediateCatchEvent','Рок',300,220);el(m.event(t,'timer'),'bpmn:timeDuration').text='P2D'
m.node('MsgEnd','endEvent','',460,40);m.node('TimerEnd','endEvent','',460,220)
m.flow('Start','Wait');m.flow('Wait','Msg',points=[(165,125),(165,58),(300,58)])
m.flow('Wait','Timer',points=[(165,175),(165,238),(300,238)]);m.flow('Msg','MsgEnd');m.flow('Timer','TimerEnd');m.save()

m=Draft('05-multi-markers','Један задатак, више извршавања')
for i,(label,seq) in enumerate([('Једном',None),('За сваку ставку, паралелно',False),('За сваку ставку, редом',True)]):
    task=m.node(f'Task{i}','task',label,40+i*240,40,w=200)
    if seq is not None:el(task,'bpmn:multiInstanceLoopCharacteristics',isSequential=str(seq).lower())
m.save()

def items(name, title, kind, label, sequential):
    m = Draft(name, title)
    m.node('Start','startEvent','',40,122)
    task = m.node('Item', kind, label, 130, 100, w=200)
    el(task, 'bpmn:multiInstanceLoopCharacteristics', isSequential=str(sequential).lower())
    m.node('Decision','exclusiveGateway','Све ставке у реду?',420,115)
    m.node('Order','sendTask','Послати наруџбину',560,30);m.node('Yes','endEvent','',800,52)
    m.node('Notify','serviceTask','Обавијестити запосленог',560,190);m.node('No','endEvent','',800,212)
    m.flow('Start','Item');m.flow('Item','Decision')
    m.flow('Decision','Order','да',[(445,115),(445,70),(560,70)])
    m.flow('Decision','Notify','не',[(445,165),(445,230),(560,230)])
    m.flow('Order','Yes');m.flow('Notify','No');m.save()

items('06-parallel-multi','Паралелно: свака ставка наруџбине','serviceTask','Провјерити ставку',False)
m = Draft('07-sequential-multi', 'Редом: референт прегледа ставку по ставку', True)
lanes = pool(m, 'Набавка', [('Референт', 160), ('Систем', 260)])
m.node('Start','startEvent','',100,82)
task = m.node('Item','userTask','Прегледати ставку',180,60,w=200)
el(task, 'bpmn:multiInstanceLoopCharacteristics', isSequential='true')
m.node('Decision','exclusiveGateway','Све ставке у реду?',440,285)
m.node('Order','sendTask','Послати наруџбину',580,200);m.node('Yes','endEvent','',840,222)
m.node('Notify','serviceTask','Обавијестити запосленог',580,340);m.node('No','endEvent','',840,362)
assign(lanes['Референт'],'Start','Item');assign(lanes['Систем'],'Decision','Order','Yes','Notify','No')
m.flow('Start','Item');m.flow('Item','Decision',points=[(280,140),(280,310),(440,310)])
m.flow('Decision','Order','да',[(465,285),(465,240),(580,240)])
m.flow('Decision','Notify','не',[(465,335),(465,380),(580,380)])
m.flow('Order','Yes');m.flow('Notify','No');m.save()

# The XOR merge keeps the first pass and the return path off the same task.
m=Draft('08-correction-loop','Понављање до потпуне наруџбине',True)
lanes=pool(m,'Набавка',[('Референт',180),('Руководилац',180)])
m.node('Start','startEvent','',100,92);m.node('Prepare','userTask','Припремити наруџбину',180,70,w=180)
m.node('Merge','exclusiveGateway','',420,85)
m.node('Fix','userTask','Допунити наруџбину',580,70,w=180)
m.node('Check','userTask','Прегледати наруџбину',480,250,w=160)
m.node('Decision','exclusiveGateway','Потпуна?',800,265);m.node('End','endEvent','',920,272)
assign(lanes['Референт'],'Start','Prepare','Merge','Fix');assign(lanes['Руководилац'],'Check','Decision','End')
m.flow('Start','Prepare');m.flow('Prepare','Merge')
m.flow('Merge','Check',points=[(445,135),(445,290),(480,290)])
m.flow('Check','Decision');m.flow('Decision','End','да')
m.flow('Decision','Fix','не',[(825,265),(825,110),(760,110)])
m.flow('Fix','Merge',points=[(580,110),(470,110)]);m.save()

m=Draft('09-reuse-kinds','Задатак и call activity')
m.node('Task','task','Задатак',40,40,w=200)
m.node('Call','callActivity','Call activity: засебан процес',280,40,w=200,calledElement='Other')
m.save()

# The caller sees one activity; the called process is a separate model in the same module.
m=Draft('10-call-activity','Набавка позива провјеру добављача')
m.node('Start','startEvent','',40,102)
m.node('Call','callActivity','Провјерити добављача',140,80,w=200,calledElement='SupplierCheck')
m.node('Decision','exclusiveGateway','Прихватљив?',420,95)
m.node('Order','sendTask','Послати наруџбину',560,20);m.node('End','endEvent','',820,42)
m.node('Notify','serviceTask','Обавијестити: добављач одбијен',560,170,w=200);m.node('Rejected','endEvent','',820,192)
m.flow('Start','Call');m.flow('Call','Decision')
m.flow('Decision','Order','да',[(445,95),(445,60),(560,60)])
m.flow('Decision','Notify','не',[(445,145),(445,210),(560,210)])
m.flow('Order','End');m.flow('Notify','Rejected');m.save()

m=Draft('11-called-process','Позвани процес: провјера добављача')
# calledElement points to this process id in the other file.
m.process.set('id','SupplierCheck')
m.plane.set('bpmnElement','SupplierCheck')
m.node('Start','startEvent','Захтјев за провјеру',40,162)
m.node('Split','parallelGateway','',130,155)
m.node('Registry','serviceTask','Провјерити регистар',255,45);m.node('Debts','serviceTask','Провјерити дугове',255,255)
m.node('Join','parallelGateway','',500,155)
m.node('Assess','userTask','Донијети оцјену',620,140);m.node('End','endEvent','Оцјена',880,162)
m.flow('Start','Split')
m.flow('Split','Registry',points=[(155,155),(155,85),(255,85)]);m.flow('Split','Debts',points=[(155,205),(155,295),(255,295)])
m.flow('Registry','Join',points=[(415,85),(525,85),(525,155)]);m.flow('Debts','Join',points=[(415,295),(525,295),(525,205)])
m.flow('Join','Assess');m.flow('Assess','End');m.save()

# Checkpoint task 3: students describe this unseen process in words.
m=Draft('12-checkpoint-return','Поврат робе',True)
lanes=pool(m,'Web продавница',[('Служба',240),('Магацин',280)],w=1600)
el(m.root,'bpmn:message',id='ReturnMessage',name='Захтјев за поврат')
st=m.node('Start','startEvent','Захтјев за поврат',100,142);m.event(st,'message',messageRef='ReturnMessage')
m.node('InTime','exclusiveGateway','У року од 14 дана?',190,135)
m.node('Reject','sendTask','Послати одбијање',300,30,w=180);m.node('RejectEnd','endEvent','',540,52)
m.node('Instructions','sendTask','Послати упутство за слање',300,120,w=180)
m.node('Receive','receiveTask','Примити пакет',540,340)
t=m.node('Timer','boundaryEvent','10 дана',600,402,attachedToRef='Receive',cancelActivity='true')
el(m.event(t,'timer'),'bpmn:timeDuration').text='P10D'
m.node('Close','serviceTask','Затворити захтјев',680,450);m.node('CloseEnd','endEvent','',900,472)
inspect=m.node('Inspect','userTask','Прегледати артикал',760,340)
el(inspect,'bpmn:multiInstanceLoopCharacteristics',isSequential='true')
m.node('Damaged','exclusiveGateway','Оштећено?',1000,355)
m.node('Agree','userTask','Договорити рјешење са купцем',1080,30,w=200);m.node('AgreeEnd','endEvent','',1340,52)
m.node('Split','parallelGateway','',1080,355)
m.node('Refund','serviceTask','Вратити новац',1200,120,w=180)
m.node('Stock','task','Вратити артикле на стање',1200,340,w=180)
m.node('Join','parallelGateway','',1440,355);m.node('End','endEvent','Поврат завршен',1530,362)
assign(lanes['Служба'],'Start','InTime','Reject','RejectEnd','Instructions','Agree','AgreeEnd','Refund')
assign(lanes['Магацин'],'Receive','Timer','Close','CloseEnd','Inspect','Damaged','Split','Stock','Join','End')
m.flow('Start','InTime')
m.flow('InTime','Reject','не',[(215,135),(215,70),(300,70)])
m.flow('InTime','Instructions','да')
m.flow('Reject','RejectEnd')
m.flow('Instructions','Receive',points=[(480,160),(510,160),(510,380),(540,380)])
m.flow('Timer','Close',points=[(618,438),(618,490),(680,490)]);m.flow('Close','CloseEnd')
m.flow('Receive','Inspect');m.flow('Inspect','Damaged')
m.flow('Damaged','Agree','да',[(1025,355),(1025,70),(1080,70)],label_at=(985,200))
m.flow('Damaged','Split','не')
m.flow('Agree','AgreeEnd')
m.flow('Split','Refund',points=[(1105,355),(1105,160),(1200,160)])
m.flow('Split','Stock')
m.flow('Refund','Join',points=[(1380,160),(1465,160),(1465,355)])
m.flow('Stock','Join');m.flow('Join','End')
# Gateway labels moved where no flow passes.
for id,(x,y) in {'InTime':(150,190),'Damaged':(960,410),'Start':(75,95)}.items():
    b=next(e for e in m.plane if e.get('id')==id+'_di').find('bpmndi:BPMNLabel/dc:Bounds',NS)
    b.set('x',str(x));b.set('y',str(y))
    if id=='Start':b.set('width','130')
m.save()

(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
text='# BPMN: трећи час — нацрти\n\nКонцептуални модели, без подешавања за извршавање.\n\n'
for item in manifest:
    name,title=item['name'],item['title']
    text+=f'## {title}\n\n![{title}]({name}.png)\n\n[BPMN]({name}.bpmn) · [SVG]({name}.svg)\n\n'
(OUT/'README.md').write_text(text)
print(f'Generated {len(manifest)} models; XML IDs and references checked.')
