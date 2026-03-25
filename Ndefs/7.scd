
Ndef(\build).clear
//BEGIN_A_CLEAN
~a_env_1 = Env.xyc([[0.0, 50, \sin] ,[0.5, 200, \sin], [1, 5000, \exp]]); //frequency
~a_env_2 = Env.xyc([[0.0, 100, \sin] ,[0.2, 200, \sin], [1, 5000, \lin]]);  //lp frequency
Ndef(\a, {| arg1 = 440, arg2 = 10000| // A
	var snd, freq, lpFreq;
	freq = arg1.lag(1);
	lpFreq = arg2.lag(1);
	snd = Saw.ar(freq);
	snd = JPverb.ar(snd);
	snd = BLowPass.ar(snd, lpFreq).sum;
	snd = snd.tanh * -1.dbamp;
	snd;
});
//END_A_CLEAN

//BEGIN_A_MOD
~a_env_1 = Env.xyc([[0.0, 50, \sin] ,[0.5, 200, \sin], [1, 5000, \exp]]); //frequency
~a_env_2 = Env.xyc([[0.0, 100, \sin] ,[0.2, 200, \sin], [1, 5000, \lin]]); //lp frequency
Ndef(\a, {|arg1 = 440, arg2 = 10000| // A
	var snd, freq, lpFreq;
	freq = arg1.lag(1) * (1 + Ndef(\b).ar);
	lpFreq = arg2.lag(1);
	snd = Saw.ar(freq);
	snd = JPverb.ar(snd) ;
	snd = BLowPass.ar(snd, lpFreq).sum;
	snd = snd.tanh * -1.dbamp;
	snd;
} ); // A
//END_A_MOD

//BEGIN_B_CLEAN
~b_env_1 = Env.xyc([[0.0, 1, \sin] , [0.4, 20, \sin],  [1, 500, \exp]]);//frequency
~b_env_2 = Env.xyc([[0.0, 100, \sin] ,[0.2, 200, \sin], [1, 5000, \lin]]); //lp frequency
Ndef(\b, {|arg1 = 440, arg2 = 10000| // A
	var snd, freq, lpFreq;
	freq = arg1.lag(1);
	lpFreq = arg2.lag(1);
	snd = Saw.ar(freq);
	snd = JPverb.ar(snd);
	snd = BLowPass.ar(snd, lpFreq).sum;
	snd = snd.tanh * -1.dbamp;
	snd;
}); // B
//END_B_CLEAN