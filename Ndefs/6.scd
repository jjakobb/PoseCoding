//BEGIN_A_CLEAN
~a_env_2 = Env.xyc([[0.0, 70, \sin] ,[0.5, 600, \sin], [1, 2000, \exp]]); //frequency
Ndef(\a, {|arg1 = 0.5, arg2 = 0.5|
	var snd = LFSaw.ar(arg2);
	snd = BLowPass.ar(snd, (arg2 * 1000 + 100));
	snd = DelayC.ar(snd, 1.1, arg2) + snd;
	//snd = BHiPass.ar(snd, snd.lag(2).range(5, 500));
	snd;
}); // A
//END_A_CLEAN

//BEGIN_A_MOD
~a_env_2 = Env.xyc([[0.0, 70, \sin] ,[0.5, 600, \sin], [1, 2000, \exp]]); //frequency
Ndef(\a, {|arg1 = 0.5, arg2 = 0.5|
	var snd = LFSaw.ar(arg2 * (1 + Ndef(\b).ar));
	snd = BLowPass.ar(snd, (arg2 * 1000 + 100));
	snd = DelayC.ar(snd, 1.1, arg2) + snd;
	//snd = BHiPass.ar(snd, snd.lag(2).range(5, 500));
	snd;
}); // A
//END_A_MOD

//BEGIN_B_CLEAN
~b_env_1 = Env.xyc([[0.0, 1, \sin] , [0.4, 20, \sin],  [1, 500, \exp]]);//frequency
Ndef(\b, {|arg1 = 0.5, arg2 = 0.5|
	var snd = LFSaw.ar(arg1);
	snd = BLowPass.ar(snd, (arg2 * 1000 + 100));
	snd = DelayC.ar(snd, 1.1, arg2) + snd;
	//snd = BHiPass.ar(snd, snd.lag(2).range(5, 500));
	snd;
}); // B
//END_B_CLEAN