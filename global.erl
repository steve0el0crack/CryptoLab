-module(global).
-export([start/0]).

start() ->
    register(vehicle, spawn(vehicle, server, [[]])),
    register(rsu, spawn(rsu, server, [[]])),
    register(tmc, spawn(tmc, server, [[]])),
    io:format("Hello world'n").
