/*
Shark chases the fishies.
Shark motion is random until a Fish is close enough.
Fishies always have a 'leader' and the other fish follow the leader.
The Fish leader's motion is random unless the Shark gets too close.
The Shark find the closest fish and if it is close enough, it attacks.
If any Fish sees the Shark get too close, it tries to escape.
When the leader is eaten, a new leader is appointed.
*/
width=400;
height=400;
void setup() {
    size(400,400);
}
var fishes = [];
var fish_count = 10;
var leader;
var shark;
var jaws;
var ATTACK_RANGE = 100;
var ESCAPE_RANGE = 100;
var ATTACK_SPEED_LIMIT = 10;
var ESCAPE_SPEED_LIMIT = 8;
var FOLLOW_SPEED_LIMIT = 1;
var right = new PVector(1,0); // used to compute rotation for shark and fleeing fish
// I don't think PVector has a det function
var det = function(v1, v2) {
    return v1.x*v2.y - v1.y*v2.x;
};

// I need the CCW angle even if > 180 degrees
var angleBetween = function(v1, v2) {
    return atan2(det(v1,v2), v1.dot(v2));
};

var vecs = [];
vecs[0] = new PVector(1,0);
vecs[1] = new PVector(1,1);
vecs[2] = new PVector(0,1);
vecs[3] = new PVector(-1,1);
vecs[4] = new PVector(-1,0);
vecs[5] = new PVector(-1,-1);
vecs[6] = new PVector(0,-1);
vecs[7] = new PVector(1,-1);
/*
for(var i=0; i<8; i++) {
    println("angleBetween "+right+", "+ vecs[i]+" is "+angleBetween(right, vecs[i]));
}

angleBetween [1, 0, 0], [1, 0, 0] is 0
angleBetween [1, 0, 0], [1, 1, 0] is 0.7853981633974483
angleBetween [1, 0, 0], [0, 1, 0] is 1.5707963267948966

angleBetween [1, 0, 0], [-1, 1, 0] is 2.356194490192345
angleBetween [1, 0, 0], [-1, 0, 0] is 3.141592653589793


angleBetween [1, 0, 0], [-1, -1, 0] is -2.356194490192345
angleBetween [1, 0, 0], [0, -1, 0] is -1.5707963267948966
angleBetween [1, 0, 0], [1, -1, 0] is -0.7853981633974483
*/

var getDrawI = function(r) {
    if (-1*PI/2 <= r && r <= PI/2) {
        return 1;
    }
    return -1;
};
angleMode = "radians";

var nominateLeader = function() {
    if (fishes.length > 0) {
        leader = fishes[random(0,fishes.length-1)];
    } else {
        leader = null;
    }
};

var Fish = function() {
  this.position = new PVector(random(width), random(height));
  this.velocity = new PVector(0, 0);
  this.acceleration = new PVector(0, 0);
  this.angle = 0;
  this.scale = new PVector(1,1);
  this.color = color(199, 123, 30);
};

// follow the leader!
Fish.prototype.follow = function(other) {
    var goal;
    if (other && other !== this) {
        goal = new PVector(other.position.x, other.position.y);
    } else {
        // if I'm the leader, move randomly
        goal = new PVector(random(0,width), random(0,height));
    }
    var dir = PVector.sub(goal, this.position);
    dir.normalize();
    dir.mult(0.2);
    this.acceleration = dir;
    this.velocity.add(this.acceleration);
    this.velocity.limit(FOLLOW_SPEED_LIMIT);
    this.position.add(this.velocity);
};

Fish.prototype.escapeFrom = function(other) {
//    println("escape from "+other.position.x);
    var goal = new PVector(other.position.x, other.position.y);
    var dir = PVector.sub(this.position, goal);
    dir.normalize();
    dir.mult(0.5);
    this.acceleration = dir;
    this.velocity.add(this.acceleration);
    this.velocity.limit(ESCAPE_SPEED_LIMIT);
    this.position.add(this.velocity);
    this.angle = angleBetween(right, this.velocity);
};

Fish.prototype.behavior = function() {
    var distToShark = this.position.dist(shark.position);
    if (distToShark < ESCAPE_RANGE) {
        this.escapeFrom(shark);
    } else {
        this.follow(leader);
    }
    this.update();
};

Fish.prototype.update = function() {
    var i = getDrawI(this.angle);
    var fishScale = new PVector(this.scale.x, this.scale.y);
    if (i < 0) {
        fishScale.y *= -1;
    }

    pushMatrix();
    translate(this.position.x, this.position.y);
    rotate(this.angle);
    scale(fishScale.x, fishScale.y);
//    println("scale "+this.scale);
    this.draw();
    popMatrix();
    this.angle = 0.0;
 //   this.scale = new PVector(1,1);
    this.checkEdges();
};

Fish.prototype.draw = function() {
    fill(this.color);
    ellipse(0, 0, 10, 5);
    triangle(-3,0,-7,4,-7,-4);
};

Fish.prototype.checkEdges = function() {
  if (this.position.x > width-20) {
    this.velocity.x *= -1;
  } 
  else if (this.position.x < 20) {
    this.velocity.x *= -1;
  }
  if (this.position.y > height-20) {
    this.velocity.y *= -1;
  } 
  else if (this.position.y < 20) {
    this.velocity.y *= -1;
  }
};

var Shark = function() {
    Fish.call(this);
    this.position.x = -30;
    this.color = color(38, 38, 191);
};

Shark.prototype = Object.create(Fish.prototype);

Shark.prototype.behavior = function() {
    
    var distToJaws = this.position.dist(jaws.position);
    if (distToJaws < ESCAPE_RANGE) {
        this.escapeFrom(jaws);
    } else {

    this.eat();
    // find the closest fish
    var distance = dist(0,0,width,height);
    var closest;
    for(var i=0; i<fishes.length; i++) {
        var d = this.position.dist(fishes[i].position);
        if (d < distance) {
            distance = d;
            closest = fishes[i];
        }
    }
    // if the closest fish is close enough, attack!
    if (distance < ATTACK_RANGE) {
        this.attack(closest);
    } else {
        this.follow(closest);
    }
    }
    this.update();
};

Shark.prototype.draw = function() {
    noStroke();
    fill(this.color);
    ellipse(0, 0, 45, 16);
    triangle(-15,0, -37,-10, -28,10);
    triangle(7,-8, -2,-17, -2,-8);
    fill(255,255,255);
    ellipse(13,-2, 3,3);
};
Shark.prototype.eat = function() {
    for(var i=fishes.length-1; i >=0; i--) {
        if (this.position.dist(fishes[i].position) < 20) {
            if ('undefined' !=== typeof getSound) {
                playSound(getSound("rpg/hit-splat"));
            }
            var goners = fishes.splice(i,1);
            if (fishes.length > 0) {
                if (goners[0] === leader) {
                    nominateLeader();
                }
            } else {
                 if ('undefined' !=== typeof getSound) {
                     playSound(getSound("rpg/water-bubble"));
                 }
                leader = this;
              //  jaws = new Jaws();
            }
        }
    }
    
};
Shark.prototype.attack = function(other) {
//    println("attack "+other);
    var goal = new PVector(other.position.x, other.position.y);
    var dir = PVector.sub(goal, this.position);
    dir.normalize();
    dir.mult(0.5);
    this.acceleration = dir;
    this.velocity.add(this.acceleration);
    this.velocity.limit(ATTACK_SPEED_LIMIT);
    this.position.add(this.velocity);
    this.angle = angleBetween(right, this.velocity);
};

var Jaws = function() {
    Shark.call(this);
    this.position.x = -130;
    this.color = color(71, 71, 71);
    this.scale = new PVector(2,2);
};

Jaws.prototype = Object.create(Shark.prototype);

Jaws.prototype.behavior = function() {
    this.eat();
    // find the shark (prey!)
    if (shark) {
        var distance = this.position.dist(shark.position);
        if (distance < ATTACK_RANGE) {
            this.attack(shark);
        } else {
            this.follow(shark);
        }
        
    } else {
     //   println("follow "+shark);
        this.follow(shark);
    }

    this.update();
};
Jaws.prototype.eat = function() {
    if (shark && this.position.dist(shark.position) < 20) {
        if ('undefined' !=== typeof getSound) {
            playSound(getSound("rpg/hit-splat"));
        }
        shark = null;
    }
};

// make some fish
var makeFish = function() {
    for (var i = 0; i < fish_count; i++) {
        fishes[i] = new Fish(i); 
    }
    shark = new Shark();
    jaws = new Jaws();
    // nominate a leader for the other fish to follow
    nominateLeader();
};

// make a shark
shark = new Shark();
jaws = new Jaws();
makeFish();

draw = function() {
    background(64, 224, 208);
    if (shark) {
        shark.behavior();
    }
    for (var i = 0; i < fishes.length; i++) {
        fishes[i].behavior();
    }
    if (fishes.length === 0) {
        jaws.behavior();
    }
};
mouseClicked = function() {
    makeFish();
};
