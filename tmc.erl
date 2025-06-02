-module(tmc).
-export([start/0]).
start() ->
    register(tmc, spawn(tmc, server, [[]])),
    io:format("Hello world'n").

server(Data) ->
    io:format("Hello world'n").
