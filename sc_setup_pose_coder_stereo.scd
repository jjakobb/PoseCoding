
ServerOptions.devices
//
s.options.device = "MADIface USB (23727305)"; //insert interface name here, obtained when executing line above
//s.options.inDevice = "Fireface UFX+ (23779253)";
s.options.numOutputBusChannels = 44;
s.options.memSize = 8192 * 4;
s.latency(0.2);
s.boot;




(
//start variables
~hand_center_dev = 0;
~hand_hight_dev = 0;
~hand_depth_dev = 0;
~hand_speed = 0;
~hand_angle = 0;
~openness = 0;
~left_hand_y = 0;
~right_hand_y = 0;
~hip_y = 1;

//Spacialization room parameters
~center = 1.5;
~hand_center_multiplier = 1.25;
~num_output_channels = 2;
)

(
//utils
~wrap_center = {|in = 0, center = 0| ((in + center - 1).wrap2(1)+1);};
//utils - specs
~spec_hand_center = ControlSpec(-2, 2);
~spec_hand_hight = ControlSpec(-3, 3.5);
~spec_hand_depth = ControlSpec(-0.6, 0.2);
~spec_openness = ControlSpec(0, 5);
~spec_hip = ControlSpec(0, 1.6);
~spec_single_hand = ControlSpec(-3.0, 3.2);
//utils - helper variables
~last_hand_height = 0;
~last_hand_center = 0;
//utils - envs
~a_env_1 = Env.xyc([[0.0, 70, \sin] ,[0.5, 600, \sin], [1, 15000, \exp]]); //frequency
~a_env_2 = Env.xyc([[0.0, 0, \sin], [1, 1.0, \exp]]); //amplitude
~b_env_1 = Env.xyc([[0.0, 70, \sin] ,[0.5, 600, \sin], [1, 15000, \exp]]);//frequency
~b_env_2 = Env.xyc([[0.0, 0, \sin], [1, 1.0, \exp]]);//amplitude

Ndef(\a, {|arg1 = 0.5, arg2 = 0.5| SinOsc.ar(60) * 0.05} ); // A
Ndef(\b, {|arg1 = 0.5, arg2 = 0.5| SinOsc.ar(61) * 0.05}); // B
Ndef(\build, { Mix.ar([Ndef(\a).ar, Ndef(\b).ar]) });
Ndef(\a).fadeTime = 4;
Ndef(\b).fadeTime = 4;

//Sound Clip
Ndef(\master, {|amp = 0.2, pos = 0|
	var snd = Ndef(\build).ar;
	//snd = SinOsc.ar() * 0.1;
	snd = snd.sum;
	snd = snd.tanh * -3.dbamp; //safety measure
	snd = PanAz.ar(~num_output_channels, snd * amp, pos);
}).play;

Ndef(\master).proxyspace.reshaping = \elastic;


//Mapping Function
Tdef(\master_link, {
	loop{
		Ndef(\master).set(\pos, ~pos );
		Ndef(\a).set(\arg1, ~a_env_1.at(~left_hand_y));
		Ndef(\a).set(\arg2, ~a_env_2.at(~openness));
		Ndef(\b).set(\arg1, ~b_env_1.at(~right_hand_y));
		Ndef(\b).set(\arg2, ~b_env_2.at(~hip_y));
		0.0001.wait;
	};
}).play;


//Recieve mapping parameters
OSCdef(\recieve_ub).enable;
OSCdef(\recieve_ub, {|msg|
	//	msg[2].postln;
	~hand_center_dev = (~spec_hand_center.unmap( msg[1]) + ~last_hand_center) / 2;
	~hand_hight_dev =  (~spec_hand_hight.unmap( msg[2] ) + ~last_hand_height) / 2;
	~hand_depth_dev = msg[3];
 	~hand_angle = ((~hand_center_dev / ~hand_depth_dev).atan()  / pi ) * 2;
 	~hand_speed = (sqrt((~last_hand_height - ~hand_hight_dev)**2 + (~last_hand_center - ~hand_center_dev)**2) +
		~hand_speed)/2;
 	~last_hand_height = ~hand_hight_dev;
 	~last_hand_center = ~hand_center_dev;
 	~openness = ~spec_openness.unmap( msg[4] );
	~pos =  ~wrap_center.value( ~hand_center_dev * ~hand_center_multiplier, ~center);
	~left_hand_y = ~spec_single_hand.unmap(msg[5] );
	~right_hand_y = ~spec_single_hand.unmap(msg[6] );
}, '/abstractions/upper_body');
OSCdef(\recieve_lb, {|msg|
	//	msg[2].postln;
	~hip_y = ~spec_hip.unmap( msg[1] );
 	//~hip_y.postln;
}, '/abstractions/lower_body');

//Recieve Executable Code
OSCdef(\recieve_code, {|msg|
	msg[1].postln;
	msg[1].asString.interpretPrint;
}, '/code/execute');

)


