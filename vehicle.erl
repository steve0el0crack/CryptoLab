-module(vehicle).
-export([start/0, server/1]).
start() ->
    register(vehicle, spawn(vehicle, server, [[]])),
    io:format("Hello world'n").

server(routes) ->
    rsu ! {self(), {"Hello world'n"}},
    receive
    {From_RSU, warning} ->
        case warning of 
            0 -> 
                io:format("Hilfe!");
            1 ->
                io:format("Achtung! Ich fahre fort")
        end
end.
