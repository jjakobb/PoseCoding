# PoseLandmark Namen
landmark_names = [
    "NOSE", "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER",
    "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER", "LEFT_EAR",
    "RIGHT_EAR", "MOUTH_LEFT", "MOUTH_RIGHT", "LEFT_SHOULDER",
    "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW", "LEFT_WRIST",
    "RIGHT_WRIST", "LEFT_PINKY", "RIGHT_PINKY", "LEFT_INDEX",
    "RIGHT_INDEX", "LEFT_THUMB", "RIGHT_THUMB", "LEFT_HIP",
    "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE",
    "RIGHT_ANKLE", "LEFT_HEEL", "RIGHT_HEEL", "LEFT_FOOT_INDEX",
    "RIGHT_FOOT_INDEX"
]

# Code Snippets
codeDict = {
    "&&Saw": """(
~env_lpFreq = Env.xyc([[0.0, 100, \sin] ,[0.2, 200, \sin], [1, 15000, \lin]]);
~env_freq = Env.xyc([[0.0, 50, \sin] ,[0.5, 200, \sin], [1, 15000, \exp]]);
Ndef(\synth).fadeTime = 0.1;
Ndef(\synth, {|amp = 0.2, freq = 440, lpFreq = 10000|
	var snd = Saw.ar(freq);
	amp = amp * XLine.ar(3, 1, 0.3);
	snd = JPverb.ar(snd) ;
	snd = BLowPass.ar(snd, lpFreq);
	Splay.ar(snd * amp);
}).play;

Tdef(\linker, {|out = 0,  arg2 = 2, arg0 = 0, arg3 = 3|
	loop{
		Ndef(\synth).set(\\amp, 0.5);
		//Ndef(\synth).set(\\freq, ~env_freq.at(~hand_hight_dev));
		Ndef(\synth).set(\\freq, ~scale_2.performNearestInScale(~hand_hight_dev * 125, 5).midicps);
		Ndef(\synth).set(\\lpFreq, ~env_lpFreq.at(~hand_center_dev));
		//(~hand_center_dev.range(4390, 19000).max(0) + 100);
		0.001.wait;
	}
}).play;
)""",
    "&&Sine": """(
~env_freq = Env.xyc([[0.0, 50, \sin] ,[0.5, 200, \sin], [1, 15000, \exp]]);
~env_dev = Env.xyc([[0.0, 0.0001, \sin] ,[0.8, 0.1, \sin], [1, 10, \lin]]);
Ndef(\synth).fadeTime = 0.1;
Ndef(\synth, {|amp = 0.2, freq = 440, dev = 0|
	var snd = SinOsc.ar(freq * [1, 1 + dev, 2, 2+(2*dev)] * [1, 5/4], [0, 0.5]);
	amp = amp * XLine.ar(3, 1, 0.3);
	snd = Mix.ar(snd / 15);
	snd = JPverb.ar(snd) ;
	Splay.ar(snd * amp);
}).play;

Tdef(\linker, {|out = 0,  arg2 = 2, arg0 = 0, arg3 = 3|
	loop{
		Ndef(\synth).set(\\amp, 0.5);
		Ndef(\synth).set(\\freq, (~scale_2.performNearestInScale(~hand_hight_dev * 125, 5)+2).midicps);
		Ndef(\synth).set(\\dev, ~env_dev.at(~hand_center_dev));
		0.001.wait;
	}
}).play;
)""",
    "&&Square": """(
~env_freq = Env.xyc([[0.0, 50, \sin] , [0.4, 100, \sin] ,[0.8, 200, \sin], [1, 500, \exp]]);
~env_dev = Env.xyc([[0.0, 0.0001, \sin] ,[0.8, 0.1, \sin], [1, 10, \lin]]);
Ndef(\synth).fadeTime = 4;
Ndef(\synth, {|amp = 0.2, freq = 440, dev = 0, pos = 0|
	var snd;
	snd = WhiteNoise.ar();
	freq = freq.lag(0.1);
	snd = (snd * 50).tanh * 0.5;
	snd = snd * Decay2.ar(Impulse.ar((dev+1)*3), 0.05,1 / (dev+1), 0.3 );
	snd = RLPF.ar(snd, freq * [1, 2, 3], 0.001 ).tanh*0.5 + RLPF.ar(snd, freq.div(50).lag(0.2)*50 * 0.5 , 0.001, 2 ).tanh*0.2;
	snd = snd + RLPF.ar(snd, freq * [1, 2, 3] * 2, 0.001 ).tanh*0.5;
	//snd = snd + RLPF.ar(snd, max(20, freq.div(50).lag(0.2)*20) , 0.001, 2 ).tanh*0.6;
	snd = snd + RLPF.ar(snd, max(20, freq.div(100).lag(0.2)*20) , 0.001, 2 ).tanh*0.6;
	snd = snd + RLPF.ar(snd, max(20, freq.div(20).lag(0.2)*40) , 0.001, 2 ).tanh*0.6;
	snd = snd.tanh* 0.8;
	snd = LeakDC.ar(snd);
	PanAz.ar(~num_output_channels, snd * amp, pos);
}).play;

Tdef(\linker, {|out = 0,  arg2 = 2, arg0 = 0, arg3 = 3|
	loop{
        Ndef(\synth).set(\\amp, 0.5);
        Ndef(\synth).set(\\freq, ~env_freq.at(~hand_hight_dev));
        Ndef(\synth).set(\\dev, ~env_dev.at(1 - ~openness));
        Ndef(\synth).set(\\pos, ~wrap_center.value( ~hand_center_dev * ~hand_center_multiplier, ~center));
		0.001.wait;
	}
}).play;
)""",
    "&&Tri": """(
~env_freq = Env.xyc([[0.0, 100, \sin] ,[0.5, 500, \sin], [1, 3000, \exp]]);
~env_dev = Env.xyc([[0.0, 3.0, \sin] ,[0.1, 1, \sin] ,[0.5, 0.0, \sin], [0.9, 1, \sin],  [1, 3.0, \lin]]);
Ndef(\synth).fadeTime = 0.1;
Ndef(\synth, {|amp = 0.2, freq = 440, t60 = 0|
	var snd = LFTri.ar(freq * [1, 1.01] * [1, 5/4], );
	amp = amp * XLine.ar(5, 1, 0.3);
	snd = JPverb.ar(snd, t60) ;
	Splay.ar(snd * amp);
}).play;

Tdef(\linker, {|out = 0,  arg2 = 2, arg0 = 0, arg3 = 3|
	loop{
		Ndef(\synth).set(\\amp, 0.5);
		Ndef(\synth).set(\\freq, (~scale_2.performNearestInScale(~hand_hight_dev * 125, 5)+5).midicps);
		Ndef(\synth).set(\\t60, ~env_dev.at(~hand_center_dev));
		0.01.wait;
	}
}).play;
)""",
    "&&Startup": "&&... Starting up ..."
}
