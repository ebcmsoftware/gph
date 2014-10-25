var printMessage =function(msg){
    document.getElementById("processingMsg").innerHTML=msg;
    };

class Time{
  int day, quarterHour;
  Time(){
  }
  void set(int x, int y){
    day=floor(x/100);
    quarterHour=floor(y/5);
  }
  void setRelative(int x, int y, Time t){
    day=floor(x/100);
    quarterHour=floor(y/5);
    if(quarterHour> t.quarterHour&&quarterHour<2+t.quarterHour)
      quarterHour=t.quarterHour+2;
  }
  boolean lessThan(Time t){
    if(day<t.day)
      return true;
    if(day>t.day)
      return false;
    if(quarterHour<t.quarterHour)
      return true;
    return false;
  }
}

ArrayList<Time> times;
ArrayList<Integer> freeTimes;
Time time1, time2;
boolean pMousePressed;
//var getStartDate(){
//  return new Date();
//}
//var getEndDate(){
//  return new Date();
//}
//var start, end;
void setup(){
  size(700,480);
  background(230);
  time1=new Time();
  time2=new Time();
  fill(80,80,200);
  times=new ArrayList<Time>();
  freeTimes=new ArrayList<Integer>();
  printMessage("hi!");
}
void draw(){
  stroke(180);
  background(230);
  for(int i=100;i<700;i+=100){
    line(i,0,i,480);
  }
  for(int i=20;i<480;i+=20){
    line(0,i,700,i);
  }
  drawTimes();
  if(mousePressed){
    time2.setRelative(mouseX, mouseY, time1);
    drawTime(time1, time2);
  }
  pMousePressed=mousePressed;
}
void mousePressed(){
  time1.set(mouseX, mouseY);
}

void mouseReleased(){
  if((time1.day==time2.day)&&(time1.quarterHour==time2.quarterHour)){
    time1=new Time();
    time2=new Time();
  }else{
    times.add(time1);
    times.add(time2);
    addTimes();
    time1=new Time();
    time2=new Time();
  }
}


void drawTimes(){
  
  for(int i=0;i<times.size();i+=2){
    Time t1=times.get(i), t2=times.get(i+1);
    fill(80,80,200);
    rect(t1.day*100, t1.quarterHour*5, (t2.day-t1.day+1)*100, t2.quarterHour*5-t1.quarterHour*5);
    //fill(255,0,0);
    int y=min(t1.quarterHour, t2.quarterHour)*5+5;
    int x=max(t1.day, t2.day)*100+75;
    strokeWeight(2);
    stroke(255,0,0);
    line(x+4,y+4,x+16,y+16);
    line(x+16,y+4,x+4,y+16);
    strokeWeight(1);
    stroke(180);
    if(mouseX<x+20&&mouseX>x&&mouseY>y&&mouseY<y+20&&mousePressed&&!pMousePressed){
      times.remove(i);
      times.remove(i);
      i-=2;
    }
  }
  
}

void drawTime(Time t1, Time t2){
  fill(80,80,200);
    rect(t1.day*100, t1.quarterHour*5, (t2.day-t1.day+1)*100, t2.quarterHour*5-t1.quarterHour*5);
}

void addTimes(){
  if(time1.lessThan(time2)){
    for(int i=time1.day;i<time2.day+1;i++){
        freeTimes.add(86400000*i+time1.quarterHour*900000);
        freeTimes.add(86400000*i+time2.quarterHour*900000);
    }
  }else{
        for(int i=time2.day;i<time1.day+1;i++){
            freeTimes.add(86400000*i+time2.quarterHour*900000);
            freeTimes.add(86400000*i+time1.quarterHour*900000);
        }
    }
  refillMessage();
}

void refillMessage(){
    String s="";
    for(int i=0;i<freeTimes.size();i++){
        s+=freeTimes.get(i)+" ";
        }
    printMessage(s);
    }
