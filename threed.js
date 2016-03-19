var Ball = function(x,y,z,d,xspeed,yspeed, zspeed) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.d = d;
    this.xspeed = xspeed;
    this.yspeed = yspeed;
    this.zspeed = zspeed;
};
Ball.prototype.draw = function() {
    // update the ball position and render it
    this.updatePosition();
    pushMatrix();
    translate(this.x, this.y, this.z);
    sphere(this.d);
    popMatrix();
};
Ball.prototype.updatePosition = function() {
    this.x += this.xspeed;
    this.y += this.yspeed;
    this.z += this.zspeed;
};
Ball.prototype.wallBounce = function() {
    if(this.x > 400 - this.d/2 || this.x < this.d/2) {

        this.xspeed *= -1;
    }
    if(this.y < this.d/2) {
        this.yspeed *= -1;
        //playSound(getSound("rpg/hit-thud"));
    }
    if(this.y > 400) {
        this.yspeed *= -1;
    }
    if (this.z > 200 || this.z < -500) {
        this.zspeed *= -1;
    }
};
Ball.prototype.reverse = function() {
    this.xspeed *= -1;
    this.yspeed *= -1;
    this.zspeed *= -1;
};

Ball.prototype.collision = function(other) {
    var vec = new PVector(this.x - other.x, this.y - other.y, this.z - other.z);
    if( vec.mag() < (this.d + other.d)) {
	this.reverse();
	// other.reverse();
    }
    return vec.mag() < (this.d + other.d);
};

var Cube = function(x,y,z,d) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.xr = -0.4;
    this.yr = 1.25;
    this.zr = 0.1;
    this.d = d;
    this.zd = 1;
};
Cube.prototype.draw = function() {
    pushMatrix();
    translate(this.x, this.y, this.z);
    rotateX(this.xr);
    rotateY(this.yr);
    rotateZ(this.zr);
    box(this.d);
    popMatrix();
};
Cube.prototype.updateRotation = function(xr,yr,zr) {
    this.xr += xr;
    this.yr += yr;
    this.zr += zr;
};
Cube.prototype.updatePosition = function() {
    this.z += this.zd;
    if (this.z < -400 || this.z > 300) {
	this.zd *= -1;
    }
};

void setup() {
    size(400,400,P3D);
    background(0);
}
var ball = new Ball(200,200,-200,20,5,5,6);
var ball2 = new Ball(175,25,-150,20,4,3,2);
var cube = new Cube(150,150, 0, 50);
var rot = 0;
void draw() {
    background(0);
    noStroke();
    fill(0,0,255);
    ball.draw();
    ball.wallBounce();
    fill(0,255,0);
    ball.collision(ball2);
    ball2.collision(ball);
    //ball.collision(cube);
    //ball2.collision(cube);
    // if(ball.collision(ball2)) {
    //println("WHAM!");
    //fill(255,0,0);
    // } else {
    //println("No");
    //fill(0,255,0);
    // }
    ball2.draw();
    ball2.wallBounce();
    // ball.collision(ball2);

    lights();
    fill(255,0,0);
    cube.updateRotation(0.003,0.01,.01);
    cube.updatePosition();
    cube.draw();
    stroke(255,255,255);
    line(0,0,-500, 400,0,-500);
    line(0,0,-500, 0,400,-500);
    line(0,400,-500,400,400,-500);
    line(400,400,-500,400,0,-500);
  
    line(0,0,-500,0,0,200);
    line(400,0,-500,400,0,200);
    line(0,400,-500,0,400,200);
    line(400,400,-500,400,400,200);
  
}