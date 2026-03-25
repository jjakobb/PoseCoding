//BEGIN_MOD
(
Ndef(\build, { Ndef(\a).ar}); // intercept  // A | B

//SLOT_B

//SLOT_A
)
//END_MOD

//BEGIN_MUL
(
Ndef(\build, { Ndef(\a).ar * Ndef(\b).ar }); // multiply  // A * B

//SLOT_B

//SLOT_A
)
//END_MUL

//BEGIN_ADD
(
Ndef(\build, { Mix.ar([Ndef(\a).ar, Ndef(\b).ar])}); // add  // A + B

//SLOT_B

//SLOT_A
)
//END_ADD