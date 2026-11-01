"""Generate the hand-laid-out, conceptual BPMN 2.0 teaching models (no engine extensions)."""
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr
import json
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '2026-2027/vjezbe/class2/bpmn-class2'
OUT.mkdir(exist_ok=True)

def attrs(**kw): return ' '.join(f'{k}={quoteattr(str(v))}' for k,v in kw.items())
class Model:
    def __init__(self, name, title):
        self.name,self.title=name,title
        self.nodes=[];self.flows=[];self.extra=[];self.colors={};self.serial=0
    def n(self,id,typ,name,x,y,w=None,h=None,parent='Process',**kw):
        if w is None: w=50 if 'Gateway' in typ else 36 if 'Event' in typ else 140
        if h is None: h=50 if 'Gateway' in typ else 36 if 'Event' in typ else 76
        self.nodes.append(dict(id=id,typ=typ,name=name,x=x,y=y,w=w,h=h,parent=parent,kw=kw));return id
    def box(self,id): return next(n for n in self.nodes if n['id']==id)
    def f(self,a,b,name='',points=None,typ='sequenceFlow'):
        self.serial+=1; id=f'Flow_{self.serial}'
        A,B=self.box(a),self.box(b)
        if points is None:
            points=[(A['x']+A['w'],A['y']+A['h']/2),(B['x'],B['y']+B['h']/2)]
        self.flows.append(dict(id=id,a=a,b=b,name=name,points=points,typ=typ,parent=A['parent']));return id
    def color(self,ids,fill='#e4f1ff',stroke='#1764a0'):
        for id in ids.split():self.colors[id]=(fill,stroke)
    def save(self, instructor=False):
        def node(n):
            kw=dict(n['kw']);expanded=kw.pop('expanded',False);definition=kw.pop('definition',None);kw.pop('label',None)
            if n['typ']=='participant':return '<bpmn:participant '+attrs(id=n['id'],name=n['name'],**kw)+'/>'
            content=''
            for f in self.flows:
                if f['typ']=='sequenceFlow':
                    if f['b']==n['id']:content+=f'<bpmn:incoming>{f["id"]}</bpmn:incoming>'
                    if f['a']==n['id']:content+=f'<bpmn:outgoing>{f["id"]}</bpmn:outgoing>'
            if definition:
                typ,properties,text=definition
                content+='<bpmn:'+typ+' '+attrs(id=n['id']+'_definition',**properties)+'>'+(f'<bpmn:timeDuration xsi:type="bpmn:tFormalExpression">{text}</bpmn:timeDuration>' if text else '')+'</bpmn:'+typ+'>'
            if n['typ']=='subProcess':content+=body(n['id'])
            return '<bpmn:'+n['typ']+' '+attrs(id=n['id'],name=n['name'],**kw)+'>'+content+'</bpmn:'+n['typ']+'>'
        def body(parent):
            content=''.join(node(n) for n in self.nodes if n['parent']==parent and n['typ']!='participant')
            for f in self.flows:
                if f['typ']=='sequenceFlow' and f['parent']==parent:
                    content+='<bpmn:sequenceFlow '+attrs(id=f['id'],sourceRef=f['a'],targetRef=f['b'],name=f['name'])+'/>'
            return content
        participants=[n for n in self.nodes if n['typ']=='participant']
        collaboration=''
        if participants:
            collaboration='<bpmn:collaboration id="Collaboration">'+''.join(node(n) for n in participants)
            collaboration+=''.join('<bpmn:messageFlow '+attrs(id=f['id'],sourceRef=f['a'],targetRef=f['b'],name=f['name'])+'/>' for f in self.flows if f['typ']=='messageFlow')+'</bpmn:collaboration>'
        xml='<?xml version="1.0" encoding="UTF-8"?>\n<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bioc="http://bpmn.io/schema/bpmn/biocolor/1.0" id="Definitions" targetNamespace="https://upp.example/teaching">'
        xml+='<bpmn:error id="InvalidArticle" name="Неважећи артикал" errorCode="NEVAZECI_ARTIKAL"/>'+''.join(self.extra)
        xml+='<bpmn:process id="Process" isExecutable="false">'+body('Process')+'</bpmn:process>'+collaboration
        xml+='<bpmndi:BPMNDiagram id="Diagram"><bpmndi:BPMNPlane id="Plane" bpmnElement="'+('Collaboration' if participants else 'Process')+'">'
        for n in self.nodes:
            expanded=n['kw'].get('expanded',False)
            props={'id':n['id']+'_di','bpmnElement':n['id']}
            if n['typ']=='exclusiveGateway':props['isMarkerVisible']='true'
            if n['typ']=='subProcess':props['isExpanded']=str(expanded).lower()
            if n['typ']=='participant':props['isHorizontal']='true'
            if n['id'] in self.colors:
                fill,stroke=self.colors[n['id']];props['bioc:fill']=fill;props['bioc:stroke']=stroke
            xml+='<bpmndi:BPMNShape '+attrs(**props)+'><dc:Bounds '+attrs(x=n['x'],y=n['y'],width=n['w'],height=n['h'])+'/>'
            if 'Event' in n['typ'] or 'Gateway' in n['typ']:
                # Stable external labels, away from connectors.
                lx,ly,lw,lh=n['kw'].get('label',(n['x']-38,n['y']+n['h']+9,n['w']+76,42))
                xml+='<bpmndi:BPMNLabel><dc:Bounds '+attrs(x=lx,y=ly,width=lw,height=lh)+'/></bpmndi:BPMNLabel>'
            xml+='</bpmndi:BPMNShape>'
        for f in self.flows:
            xml+='<bpmndi:BPMNEdge '+attrs(id=f['id']+'_di',bpmnElement=f['id'])+'>'+''.join('<di:waypoint '+attrs(x=x,y=y)+'/>' for x,y in f['points'])
            if f['name']:
                segments=list(zip(f['points'],f['points'][1:]))
                (x1,y1),(x2,y2)=max(segments,key=lambda p:abs(p[1][0]-p[0][0])+abs(p[1][1]-p[0][1]))
                vertical=abs(y2-y1)>abs(x2-x1)
                lx=(x1+x2)/2+10 if vertical else (x1+x2)/2-48
                ly=(y1+y2)/2-12 if vertical else (y1+y2)/2-28
                if f['typ']=='messageFlow':ly=105
                xml+='<bpmndi:BPMNLabel><dc:Bounds '+attrs(x=lx,y=ly,width=96,height=24)+'/></bpmndi:BPMNLabel>'
            xml+='</bpmndi:BPMNEdge>'
        xml+='</bpmndi:BPMNPlane></bpmndi:BPMNDiagram></bpmn:definitions>'
        name=('instructor/' if instructor else '')+self.name
        target=OUT/(name+'.bpmn')
        target.parent.mkdir(exist_ok=True)
        target.write_text(xml)
        manifest.append(dict(name=name,title=self.title,audience='instructor' if instructor else 'student',fontSize=getattr(self,'font_size',16)))
manifest=[]

def linear(name,title,labels):
    m=Model(name,title);m.n('Start','startEvent','',40,112);prev='Start'
    for i,label in enumerate(labels):
        id=f'Task_{i}';m.n(id,'task',label,120+i*200,92);m.f(prev,id);prev=id
    m.n('End','endEvent','',120+len(labels)*200,112);m.f(prev,'End');return m

m=linear('01-starter','Почетна скица: правила тек треба разјаснити',['Примити захтјев','Провјерити услове','Наручити робу','Обавијестити запосленог']);m.save()
# Approval XOR, one local fragment with all normal outcomes.
m=Model('02-approval','Износ и одлука руководиоца')
m.n('Start','startEvent','',30,202);m.n('Amount','exclusiveGateway','Преко 1.000 €?',130,195)
m.n('Approve','userTask','Одобрити набавку',270,182);m.n('Decision','exclusiveGateway','Одобрено?',485,195)
m.n('Merge','exclusiveGateway','',700,195);m.n('Next','task','Провјерити услове',820,182);m.n('End','endEvent','',1030,202)
m.n('Notify','sendTask','Обавијестити: одбијено',650,30,180);m.n('Rejected','endEvent','',1030,50)
m.f('Start','Amount');m.f('Amount','Approve','да')
m.f('Amount','Merge','не',[(155,245),(155,380),(725,380),(725,245)])
m.f('Approve','Decision');m.f('Decision','Merge','да')
m.f('Decision','Notify','не',[(510,195),(510,68),(650,68)])
m.f('Notify','Rejected');m.f('Merge','Next');m.f('Next','End');m.save()

def checks(name,title,split='parallelGateway',join='parallelGateway',state=False):
    m=Model(name,title);m.n('Start','startEvent','',30,162);m.n('Split',split,'',130,155)
    m.n('Budget','serviceTask','Провјерити буџет',255,45);m.n('Stock','serviceTask','Провјерити доступност',255,255)
    m.n('Join',join,'',500,155);m.n('Result','exclusiveGateway','Оба позитивна?',630,155)
    m.n('Order','task','Наставити набавку',765,45);m.n('Notify','sendTask','Обавијестити: нема услова',765,255)
    m.n('YesEnd','endEvent','',965,65);m.n('NoEnd','endEvent','',965,275)
    m.f('Start','Split');m.f('Split','Budget','',[(155,155),(155,83),(255,83)]);m.f('Split','Stock','',[(155,205),(155,293),(255,293)])
    m.f('Budget','Join','',[(395,83),(525,83),(525,155)]);m.f('Stock','Join','',[(395,293),(525,293),(525,205)])
    m.f('Join','Result');m.f('Result','Order','да',[(655,155),(655,83),(765,83)]);m.f('Result','Notify','не',[(655,205),(655,293),(765,293)])
    m.f('Order','YesEnd');m.f('Notify','NoEnd')
    if state:m.color('Budget','#ffffff','#8a94a3');m.color('Stock','#e6f1fb','#1565a9');m.color('Join','#ffffff','#8a94a3')
    return m
checks('03-parallel','Двије провјере, па одлука').save()
checks('04-waiting','Стање: буџет је провјерен, доступност још траје',state=True).save()
checks('05-wrong-xor-and','Намјерна грешка: бира се једна грана, а чекају обје',split='exclusiveGateway').save()
checks('06-wrong-and-xor','Намјерна грешка: двије гране, без синхронизације',join='exclusiveGateway').save()

# Receiving a supplier reply is an activity, so its timeout uses the same
# boundary-timer pattern as approval. No event-based gateway is needed.
m=Model('08-supplier','Пријем одговора са роком од 24 часа')
m.extra=['<bpmn:message id="SupplierReply" name="Одговор добављача"/>']
m.n('Supplier','participant','Добављач',30,20,1120,65,parent='Collaboration')
m.n('Office','participant','Служба набавке',30,145,1120,400,parent='Collaboration',processRef='Process')
m.n('Start','startEvent','',80,237)
m.n('Send','sendTask','Послати упит',180,217,140)
m.n('Reply','receiveTask','Примити одговор',430,217,180,messageRef='SupplierReply')
m.n('Deadline','boundaryEvent','24 часа',500,275,attachedToRef='Reply',cancelActivity='true',definition=('timerEventDefinition',{},'PT24H'))
m.box('Deadline')['kw']['label']=(380,325,115,28)
m.n('Decision','exclusiveGateway','Прихвата?',700,230)
m.box('Decision')['kw']['label']=(730,292,110,35)
m.n('Order','sendTask','Наручити робу',900,217,170)
m.n('Notify','sendTask','Обавијестити запосленог',850,425,190)
m.n('Done','endEvent','',1090,445)
m.f('Start','Send');m.f('Send','Reply');m.f('Reply','Decision');m.f('Decision','Order','да')
m.f('Order','Notify','',[(985,293),(985,370),(945,370),(945,425)])
m.f('Decision','Notify','не',[(725,280),(725,463),(850,463)])
m.f('Deadline','Notify','',[(518,311),(518,525),(945,525),(945,501)])
# Both failed reception and a negative answer share the notification activity;
# an activity with multiple alternative incoming flows does not synchronize.
m.f('Notify','Done')
m.f('Send','Supplier','упит',[(250,217),(250,85)],typ='messageFlow')
m.f('Supplier','Reply','одговор + ID',[(550,85),(550,217)],typ='messageFlow')
m.f('Order','Supplier','поруџбина',[(985,217),(985,85)],typ='messageFlow')
m.save()

m=Model('10-boundary-timers','Подсјетник оставља задатак активним; рок га прекида')
m.n('Start','startEvent','',40,52);m.n('Approve','userTask','Одобрити набавку',220,32,280,110)
m.n('Decision','exclusiveGateway','Одобрено?',650,45);m.n('Continue','task','Наставити набавку',800,32);m.n('Done','endEvent','',1010,52)
m.n('Reminder','boundaryEvent','1 дан',270,124,attachedToRef='Approve',cancelActivity='false',definition=('timerEventDefinition',{},'P1D'))
m.n('Deadline','boundaryEvent','2 дана',420,124,attachedToRef='Approve',cancelActivity='true',definition=('timerEventDefinition',{},'P2D'))
m.n('Email','sendTask','Послати подсјетник',200,280,170);m.n('ReminderEnd','endEvent','',470,300)
m.n('Close','sendTask','Обавијестити: затворено',650,280,190);m.n('Closed','endEvent','',950,300)
m.box('Reminder')['kw']['label']=(175,175,100,28);m.box('Deadline')['kw']['label']=(450,175,100,28)
m.f('Start','Approve','',[(76,70),(145,70),(145,87),(220,87)]);m.f('Approve','Decision','',[(500,87),(575,87),(575,70),(650,70)]);m.f('Decision','Continue','да');m.f('Continue','Done')
m.f('Reminder','Email','',[(288,160),(288,280)])
m.f('Deadline','Close','',[(438,160),(438,235),(745,235),(745,280)])
m.f('Decision','Close','не',[(675,95),(675,205),(780,205),(780,280)])
m.f('Email','ReminderEnd');m.f('Close','Closed');m.save()

def subprocess(name,title):
    m=Model(name,title)
    m.n('Sub','subProcess','Провјерити услове набавке',110,30,760,390,expanded=True)
    par='Sub'
    m.n('InnerStart','startEvent','',140,207,parent=par);m.n('Fork','parallelGateway','',220,200,parent=par)
    m.n('Budget','serviceTask','Провјерити буџет',335,85,155,parent=par)
    m.n('Stock','serviceTask','Провјерити доступност',335,275,155,parent=par)
    m.n('Valid','exclusiveGateway','Шифра исправна?',550,288,parent=par)
    m.n('Join','parallelGateway','',700,130,parent=par);m.n('InnerEnd','endEvent','',795,137,parent=par)
    m.n('Error','endEvent','Неважећи артикал',690,327,parent=par,definition=('errorEventDefinition',{'errorRef':'InvalidArticle'},''))
    m.n('Start','startEvent','',25,207);m.n('Catch','boundaryEvent','NEVAZECI_ARTIKAL',410,402,attachedToRef='Sub',cancelActivity='true',definition=('errorEventDefinition',{'errorRef':'InvalidArticle'},''))
    m.n('Next','task','Провјерити резултате',925,185,170);m.n('End','endEvent','',1140,205)
    m.n('Notify','sendTask','Затражити исправљен захтјев',600,490,195);m.n('InvalidEnd','endEvent','',940,510)
    m.box('Catch')['kw']['label']=(180,450,210,35)
    m.f('Start','Sub');m.f('Sub','Next');m.f('Next','End')
    m.f('InnerStart','Fork');m.f('Fork','Budget','',[(245,200),(245,123),(335,123)])
    m.f('Fork','Stock','',[(245,250),(245,313),(335,313)])
    m.f('Budget','Join','',[(490,123),(725,123),(725,130)])
    m.f('Stock','Valid');m.f('Valid','Join','да',[(575,288),(575,220),(725,220),(725,180)])
    m.f('Valid','Error','не',[(575,338),(575,345),(690,345)])
    m.f('Join','InnerEnd');m.f('Catch','Notify','',[(428,438),(428,528),(600,528)]);m.f('Notify','InvalidEnd')
    return m
subprocess('11-error-scope','Грешка прекида цијели потпроцес провјера').save()
m=subprocess('12-error-active','Сценарио: грешка у доступности, буџет још активан')
m.color('Stock Valid Error Catch Notify InvalidEnd','#fde7e5','#b3261e');m.color('Budget','#eeeeee','#777777');m.save()
m=linear('13-collapsed','Исти опсег, склопљен приказ',['Примити захтјев','Провјерити услове','Наставити набавку'])
m.box('Task_1')['typ']='subProcess';m.save()

# One connected baseline: all business outcomes reach notification exactly once.
m=Model('17-base-overview','Основни модел набавке: повезана цјелина')
m.n('Start','startEvent','',20,192)
m.n('Amount','exclusiveGateway','Преко 1.000 €?',100,185)
m.n('Approve','userTask','Одобрити набавку',220,172,150)
m.n('Approved','exclusiveGateway','Одобрено?',430,185)
m.n('Merge','exclusiveGateway','',570,185)
m.n('Fork','parallelGateway','',690,185)
m.n('Budget','serviceTask','Провјерити буџет',800,50,160)
m.n('Stock','serviceTask','Провјерити доступност',800,300,160)
m.n('Join','parallelGateway','',1040,185)
m.n('Results','exclusiveGateway','Оба позитивна?',1150,185)
m.n('Order','sendTask','Наручити робу',1280,172,160)
m.n('Outcomes','exclusiveGateway','',1000,553)
m.n('Notice','sendTask','Обавијестити запосленог',750,540,180)
m.n('End','endEvent','',620,560)
m.f('Start','Amount');m.f('Amount','Approve','да');m.f('Approve','Approved')
m.f('Amount','Merge','не',[(125,185),(125,10),(595,10),(595,185)])
m.f('Approved','Merge','да');m.f('Merge','Fork')
m.f('Approved','Outcomes','не',[(455,235),(455,680),(1025,680),(1025,603)])
m.f('Fork','Budget','',[(715,185),(715,88),(800,88)])
m.f('Fork','Stock','',[(715,235),(715,338),(800,338)])
m.f('Budget','Join','',[(960,88),(1065,88),(1065,185)])
m.f('Stock','Join','',[(960,338),(1065,338),(1065,235)])
m.f('Join','Results');m.f('Results','Order','да')
m.f('Results','Outcomes','не',[(1175,235),(1175,400),(1025,400),(1025,553)])
m.f('Order','Outcomes','',[(1360,248),(1360,578),(1050,578)])
m.f('Outcomes','Notice','',[(1000,578),(930,578)])
m.f('Notice','End','',[(750,578),(656,578)])
m.save()

# Worked B solution: show only after students attempt the task.
m=subprocess('19-shared-deadline-solution','Рјешење: заједнички рок обје провјере')
m.box('Catch').update(x=210)
m.box('Catch')['name']='Неважећи артикал'
m.box('Catch')['kw']['label']=(65,450,135,50)
m.box('Notify').update(x=110,y=610,w=190)
m.box('InvalidEnd').update(x=370,y=630)
m.box('Next').update(x=1080,y=200,w=50,h=50,typ='exclusiveGateway',name='Оба позитивна?')
m.box('Next')['kw']['label']=(1140,280,140,35)
m.box('End').update(x=1460,y=430)
# Replace only the outer connections; inner parallel checks stay unchanged.
m.flows=[f for f in m.flows if (f['a'],f['b']) not in [('Sub','Next'),('Next','End'),('Catch','Notify'),('Notify','InvalidEnd')]]
m.n('Reminder','boundaryEvent','24 часа',410,402,attachedToRef='Sub',cancelActivity='false',definition=('timerEventDefinition',{},'PT24H'))
m.n('Deadline','boundaryEvent','48 часова',610,402,attachedToRef='Sub',cancelActivity='true',definition=('timerEventDefinition',{},'PT48H'))
m.box('Reminder')['kw']['label']=(440,450,110,30)
m.box('Deadline')['kw']['label']=(640,450,110,30)
m.n('ReminderTask','sendTask','Послати подсјетник',450,610,170)
m.n('ReminderEnd','endEvent','',700,630)
m.n('Manual','userTask','Ручно\nпровјерити услове',900,610,190)
m.n('RecoveryMerge','exclusiveGateway','',965,200)
m.n('Order','sendTask','Наручити робу',1210,187,170)
m.n('OutcomeNotice','sendTask','Обавијестити запосленог',1210,410,190)
m.f('Sub','RecoveryMerge');m.f('RecoveryMerge','Next')
m.f('Next','Order','да')
m.f('Next','OutcomeNotice','не',[(1105,250),(1105,448),(1210,448)])
m.f('Order','OutcomeNotice','',[(1295,263),(1295,350),(1305,350),(1305,410)])
m.f('OutcomeNotice','End')
m.f('Catch','Notify','',[(228,438),(228,610)]);m.f('Notify','InvalidEnd')
m.f('Reminder','ReminderTask','',[(428,438),(428,550),(535,550),(535,610)])
m.f('ReminderTask','ReminderEnd')
m.f('Deadline','Manual','',[(628,438),(628,520),(995,520),(995,610)])
m.f('Manual','RecoveryMerge','',[(1090,648),(1560,648),(1560,105),(990,105),(990,200)])
m.save()

# Micro examples reveal one construct at a time, not the assembled task answer.
m=linear('20-sequence','Почетак, задатак, крај',['Обрадити захтјев'])
m.save()

m=Model('21-minimal-xor','XOR: једна од двије путање')
m.n('Start','startEvent','',25,162)
m.n('Choice','exclusiveGateway','Одобрено?',145,155)
m.n('Continue','task','Наставити обраду',290,35,175)
m.n('Reject','sendTask','Обавијестити: одбијено',290,265,175)
m.n('YesEnd','endEvent','',550,55);m.n('NoEnd','endEvent','',550,285)
m.f('Start','Choice');m.f('Choice','Continue','да',[(170,155),(170,73),(290,73)])
m.f('Choice','Reject','не',[(170,205),(170,303),(290,303)])
m.f('Continue','YesEnd');m.f('Reject','NoEnd');m.save()

def minimal_parallel(name,title,budget='Провјерити буџет',stock='Провјерити доступност'):
    m=Model(name,title)
    m.n('Start','startEvent','',25,162);m.n('Fork','parallelGateway','',135,155)
    m.n('Budget','task',budget,275,45,175);m.n('Stock','task',stock,275,255,175)
    m.n('Join','parallelGateway','',560,155);m.n('End','endEvent','',720,162)
    m.f('Start','Fork');m.f('Fork','Budget','',[(160,155),(160,83),(275,83)])
    m.f('Fork','Stock','',[(160,205),(160,293),(275,293)])
    m.f('Budget','Join','',[(450,83),(585,83),(585,155)])
    m.f('Stock','Join','',[(450,293),(585,293),(585,205)])
    m.f('Join','End');return m
minimal_parallel('22-minimal-and','AND: покренути обје, сачекати обје').save()

for interrupting in [True,False]:
    name='23-interrupting' if interrupting else '24-noninterrupting'
    m=Model(name,'Прекидни тајмер' if interrupting else 'Непрекидни тајмер')
    m.n('Start','startEvent','',25,82)
    m.n('Review','userTask','Одобрити набавку',180,62,220,100)
    m.n('Done','endEvent','',650,94)
    m.n('Timer','boundaryEvent','2 дана' if interrupting else '1 дан',272,144,
        attachedToRef='Review',cancelActivity='true' if interrupting else 'false',
        definition=('timerEventDefinition',{},'P2D' if interrupting else 'P1D'))
    m.box('Timer')['kw']['label']=(145,195,120,30)
    m.n('Handle','sendTask','Обавијестити: затворено' if interrupting else 'Послати подсјетник',350,315,200)
    m.n('HandlerEnd','endEvent','',650,335)
    m.f('Start','Review','',[(61,100),(120,100),(120,112),(180,112)])
    m.f('Review','Done');m.f('Timer','Handle','',[(290,180),(290,353),(350,353)])
    m.f('Handle','HandlerEnd');m.save()

m=Model('25-minimal-error','Потпроцес: нормалан исход и грешка')
m.n('Sub','subProcess','Провјерити артикал',110,30,660,340,expanded=True)
m.n('InnerStart','startEvent','',140,160,parent='Sub')
m.n('Check','task','Провјерити шифру',235,140,150,parent='Sub')
m.n('Valid','exclusiveGateway','Шифра исправна?',455,153,parent='Sub')
m.box('Valid')['kw']['label']=(330,235,125,30)
m.n('NormalEnd','endEvent','',640,63,parent='Sub')
m.n('ErrorEnd','endEvent','Неважећа шифра',640,263,parent='Sub',definition=('errorEventDefinition',{'errorRef':'InvalidArticle'},''))
m.n('Start','startEvent','',25,182)
m.n('Catch','boundaryEvent','Грешка',410,352,attachedToRef='Sub',cancelActivity='true',definition=('errorEventDefinition',{'errorRef':'InvalidArticle'},''))
m.box('Catch')['kw']['label']=(290,400,100,30)
m.n('Next','task','Наставити обраду',850,162,160);m.n('End','endEvent','',1080,182)
m.n('Notice','sendTask','Затражити исправку',550,465,180);m.n('ErrorDone','endEvent','',850,485)
m.f('Start','Sub');m.f('Sub','Next');m.f('Next','End')
m.f('InnerStart','Check');m.f('Check','Valid')
m.f('Valid','NormalEnd','да',[(480,153),(480,81),(640,81)])
m.f('Valid','ErrorEnd','не',[(480,203),(480,281),(640,281)])
m.f('Catch','Notice','',[(428,388),(428,503),(550,503)]);m.f('Notice','ErrorDone');m.save()

m=minimal_parallel('26-wrong-timer-scope','Намјерна грешка: рок је само на једној провјери')
m.n('Timer','boundaryEvent','48 часова',342,27,attachedToRef='Budget',cancelActivity='true',definition=('timerEventDefinition',{},'PT48H'))
m.box('Timer')['kw']['label']=(195,-10,120,30)
m.n('Manual','userTask','Ручно провјерити услове',550,-138,220)
m.n('ManualEnd','endEvent','',870,-118)
m.f('Timer','Manual','',[(360,27),(360,-100),(550,-100)]);m.f('Manual','ManualEnd');m.save()

m=minimal_parallel('28-exit-preparation','Самостално: рок припреме испоруке','Припремити робу','Припремити документа')
m.save()

# An enlarged, collapsed view of the normal/timeout paths in solution B.
# Other boundary paths are shown on the complete model and the boundary close-up.
m=Model('32-manual-return','Рјешење B: нормалан и ручни наставак')
m.font_size=18
m.n('Sub','subProcess','Провјерити услове',30,30,200,100)
m.n('Deadline','boundaryEvent','48 часова',62,112,attachedToRef='Sub',cancelActivity='true',definition=('timerEventDefinition',{},'PT48H'))
m.box('Deadline')['kw']['label']=(105,175,115,30)
m.n('Manual','userTask','Ручно\nпровјерити услове',240,250,190,90)
m.n('Merge','exclusiveGateway','',450,55)
m.n('Results','exclusiveGateway','Оба позитивна?',570,55)
m.box('Results')['kw']['label']=(615,130,105,45)
m.n('Order','sendTask','Наручити робу',700,35,190,90)
m.n('Notice','sendTask','Обавијестити запосленог',700,250,190,90)
m.n('End','endEvent','',950,277)
m.f('Sub','Merge');m.f('Deadline','Manual','',[(80,148),(80,295),(240,295)])
m.f('Manual','Merge','',[(430,295),(475,295),(475,105)])
m.f('Merge','Results');m.f('Results','Order','да')
m.f('Results','Notice','не',[(595,105),(595,295),(700,295)])
m.f('Order','Notice','',[(795,125),(795,250)]);m.f('Notice','End');m.save()

m=Model('33-xor-merge','Спајање алтернативних путања')
m.n('Start','startEvent','',25,162);m.n('Choice','exclusiveGateway','Ручни преглед?',145,155)
m.box('Choice')['kw']['label']=(35,220,115,40)
m.n('Manual','userTask','Прегледати ручно',290,35,175)
m.n('Auto','serviceTask','Провјерити аутоматски',290,265,175)
m.n('Merge','exclusiveGateway','',560,155)
m.n('Next','task','Наставити обраду',690,142,175)
m.n('End','endEvent','',940,162)
m.f('Start','Choice');m.f('Choice','Manual','да',[(170,155),(170,73),(290,73)])
m.f('Choice','Auto','не',[(170,205),(170,303),(290,303)])
m.f('Manual','Merge','',[(465,73),(585,73),(585,155)])
m.f('Auto','Merge','',[(465,303),(585,303),(585,205)])
m.f('Merge','Next');m.f('Next','End');m.save()

# The same parallel process in three execution states, with work after the join.
m=minimal_parallel('34-and-execution','Паралелне провјере и заједнички наставак')
m.box('End').update(x=940)
m.flows=[f for f in m.flows if (f['a'],f['b'])!=('Join','End')]
m.n('Next','task','Наставити обраду',700,142,160)
m.f('Join','Next');m.f('Next','End');m.save()
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'Generated {len(manifest)} editable BPMN models')

index = '# BPMN dijagrami: drugi čas\n\nModeli se otvaraju u Camunda Modeler-u ili na [bpmn.io](https://demo.bpmn.io/).\nModeli su konceptualni, bez podešavanja za izvršavanje.\n\nDijagrami 05 i 06 su namjerno pogrešni primjeri za analizu.\nBoje su ilustracija scenarija, ne dodatna BPMN notacija ni simulacija.\n\n'
for item in manifest:
    if item['audience']=='instructor':continue
    name,title=item['name'],item['title']
    index+=f'## {title}\n\n![{title}]({name}.png)\n\n[Model za uređivanje]({name}.bpmn) · [SVG]({name}.svg) · [PNG]({name}.png)\n\n'
index+='Generisano pomoću [bpmn-js](https://bpmn.io/toolkit/bpmn-js/).\n[Uputstvo za regenerisanje](../../../../tools/bpmn/README.md).\n'
(OUT/'README.md').write_text(index)
