/* @pjs preload="x-wing.gif,tie-fighter.jpg"; */
var b;
var t;
void setup() {
  size(450,450);
  b = loadImage("x-wing.gif");
  t = loadImage("tie-fighter.jpg");
  //noLoop();
}
var XWing = function(x, y) {
    this.position = new PVector(x, y);
};
XWing.prototype.draw = function() {
    pushMatix();
    translate(200,300);
    scale(0.5, 0.5);
    image(b, 0,0);
    popMatrix();
    //println("mouseX:"+mouseX);
};
var Fighter = function(x, y) {
    this.position = new PVector(x,y);
    this.velocity = new PVector(0,0);
};
Fighter.prototype.draw = function() {
    pushMatix();
    translate(this.position.x, this.position.y);
    image(t, 0,0);
    popMatrix();
    
};
Fighter.prototype.update = function() {
    this.velocity.add(new PVector(1,1));
    this.position.add(this.velocity);
};
var xwing = new XWing(0,0);
var fighter = new Fighter(0,0);
var draw=function() {
    xwing.draw();
    fighter.update();
    fighter.draw();
  //image(b, 200,200);
  
  //image(t, 100,100);
};
