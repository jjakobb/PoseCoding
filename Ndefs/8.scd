//BEGIN_A_CLEAN
~a_env_1 = Env.xyc([[0.0, 50, \sin] , [0.4, 100, \sin] ,[0.8, 200, \sin], [1, 500, \exp]]); //frequency
~a_env_2 = Env.xyc([[0.0, 0.0001, \sin] ,[0.8, 0.1, \sin], [1, 10, \lin]]); //deviation
Ndef(\a, {|arg1 = 440, arg2 = 0|
	var snd, freq, dev;
	snd = WhiteNoise.ar();
	dev = arg2.lag(0.2);
	freq = arg1.lag(0.1);
	snd = (snd * 50).tanh * 0.5;
	snd = snd * Decay2.ar(Impulse.ar((dev+1)*3), 0.05,1 / (dev+1), 0.3 );
	snd = RLPF.ar(snd, freq * [1, 2, 3], 0.001 ).tanh*0.5 + RLPF.ar(snd, freq.div(50).lag(0.2)*50 * 0.5 , 0.001, 2 ).tanh*0.2;
	snd = snd + RLPF.ar(snd, freq * [1, 2, 3] * 2, 0.001 ).tanh*0.5;
	//snd = snd + RLPF.ar(snd, max(20, freq.div(50).lag(0.2)*20) , 0.001, 2 ).tanh*0.6;
	snd = snd + RLPF.ar(snd, max(20, freq.div(100).lag(0.2)*20) , 0.001, 2 ).tanh*0.6;
	snd = snd + RLPF.ar(snd, max(20, freq.div(20).lag(0.2)*40) , 0.001, 2 ).tanh*0.6;
	snd = Mix.ar(snd);
	snd = LeakDC.ar(snd);
	snd = snd.tanh * -1.dbamp;

});
//END_A_CLEAN

//BEGIN_A_MOD
~a_env_1 = Env.xyc([[0.0, 50, \sin] , [0.4, 100, \sin] ,[0.8, 200, \sin], [1, 500, \exp]]); //frequency
~a_env_2 = Env.xyc([[0.0, 0.0001, \sin] ,[0.8, 0.1, \sin], [1, 10, \lin]]); //deviation
Ndef(\a, {|arg1 = 440, arg2 = 0|  // A
	var snd, freq, dev;
	snd = (WhiteNoise.ar() + Ndef(\b).ar)/2;
	dev = arg2.lag(0.2);
	freq = arg1.lag(0.1);
	snd = (snd * 50).tanh * 0.5;
	snd = snd * Decay2.ar(Impulse.ar((dev+1)*3), 0.05,1 / (dev+1), 0.3 );
	snd = RLPF.ar(snd, freq * [1, 2, 3], 0.001 ).tanh*0.5 + RLPF.ar(snd, freq.div(50).lag(0.2)*50 * 0.5 , 0.001, 2 ).tanh*0.2;
	snd = snd + RLPF.ar(snd, freq * [1, 2, 3] * 2, 0.001 ).tanh*0.5;
	//snd = snd + RLPF.ar(snd, max(20, freq.div(50).lag(0.2)*20) , 0.001, 2 ).tanh*0.6;
	snd = snd + RLPF.ar(snd, max(20, freq.div(100).lag(0.2)*20) , 0.001, 2 ).tanh*0.6;
	snd = snd + RLPF.ar(snd, max(20, freq.div(20).lag(0.2)*40) , 0.001, 2 ).tanh*0.6;
	snd = Mix.ar(snd);
	snd = LeakDC.ar(snd);
	snd = snd.tanh * -1.dbamp;
});
//END_A_MOD

//BEGIN_B_CLEAN
~b_env_1 = Env.xyc([[0.0, 1, \sin] , [0.4, 20, \sin],  [1, 500, \exp]]);//frequency
~b_env_2 = Env.xyc([[0.0, 0.0001, \sin] ,[0.8, 0.1, \sin], [1, 10, \lin]]); //deviation
Ndef(\b, {|arg1 = 440, arg2 = 0| // B
	var snd, freq, dev;
	snd = WhiteNoise.ar();
	dev = arg2.lag(0.2);
	freq = arg1.lag(0.1);
	snd = (snd * 50).tanh * 0.5;
	snd = snd * Decay2.ar(Impulse.ar((dev+1)*3), 0.05,1 / (dev+1), 0.3 );
	snd = RLPF.ar(snd, freq * [1, 2, 3], 0.001 ).tanh*0.5 + RLPF.ar(snd, freq.div(50).lag(0.2)*50 * 0.5 , 0.001, 2 ).tanh*0.2;
	snd = snd + RLPF.ar(snd, freq * [1, 2, 3] * 2, 0.001 ).tanh*0.5;
	//snd = snd + RLPF.ar(snd, max(20, freq.div(50).lag(0.2)*20) , 0.001, 2 ).tanh*0.6;
	snd = snd + RLPF.ar(snd, max(20, freq.div(100).lag(0.2)*20) , 0.001, 2 ).tanh * 0.6;
	snd = snd + RLPF.ar(snd, max(20, freq.div(20).lag(0.2)*40) , 0.001, 2 ).tanh * 0.6;
	snd = Mix.ar(snd);
	snd = LeakDC.ar(snd);
	snd = snd.tanh * -1.dbamp;
});
//END_B_CLEAN