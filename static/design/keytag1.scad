/*
 * Personal Key Chain
 *   v1.0
 *   December 2015
 *   by Jonathan Meyer (jon@stej.com)
 */

// preview[view:south, tilt:top]

// The name to display on the key chain.
custom_text_1 = "Jonathan";

/* [Font] */

// The font to write the name in.
font = 0; // [0:Google (give name below), 1:Helvetica, 2:Times, 3:Arial, 4:Courier]

// the name of the font to get from https://www.google.com/fonts/
google_font = "Tangerine";

// The Font Style. Not all styles work with all fonts.
style = 2; // [0:None, 1:Regular, 2:Bold, 3:Italic, 4:Bold Italic]

/* [Size] */

// How tall the key chain will be.
width = 20; // [15:30]

// How long the key chain will be.
length = 50;  // [40:100]

// How thick the key chain will be.
thickness = 5; // [3:10]

// How round the corners will be
roundness = 2;   // [1:5]

/* [Hidden] */

font_list = [undef,
             "Helvetica",
             "Times",
             "Arial",
             "Courier"
             ];

style_list = [undef,
              "Regular",
              "Bold",
              "Italic",
              "Bold Italic"];

w = width;
l = length;
d = thickness;
r = roundness;
t = custom_text_1;

fn = (font == 0) ? google_font : font_list[font];
sn = (style_list[style] != undef) ? str(":style=",style_list[style]) : "";
f = str(fn,sn);

echo(str("Font Used -> ", f));

union(){
  difference(){
    hull(){
      translate([-((w/2)+(l/2)-2.5),0,0])
      minkowski(){
        cylinder(h=d-r,d=w, center=true, $fn=100);
        sphere(d=r, $fn=100);
      }

      minkowski(){
        cube([l,w,d-r],true);
        sphere(d=r, $fn=100);
      }
    }

    translate([-((w/2)+(l/2)-2.5),0,0])
    cylinder(h=d,d=w-5, center=true, $fn=100);

    translate([0,0,0])
    linear_extrude(height=d/2)
    text(t, valign="center", halign="center", font=f, $fn=100);
  }

 // color([0,1,0,1])
 // translate([0,0,(-d/2)+.3])
 // linear_extrude(height=d/2)
 // text(t, valign="center", halign="center", font=f);
}
