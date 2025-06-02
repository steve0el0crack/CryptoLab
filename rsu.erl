-module(rsu).
-export([start/0, server/1]).
start() ->
    register(rsu, spawn(rsu, server, [[]])),
    io:format("Hello world'n").

routes = []

server(Data) ->
    receive
    {From, {route}} ->
        From ! {rsu, ok},
        server(deposit(Who, Amount, Data));
        end
end.
lookup(Who, [{Who, Value}|_]) -> Value;
lookup(Who, [_|T]) -> lookup(Who, T);
lookup(_, _) -> undefined.

deposit(Who, X, [{Who, Balance}|T]) ->
    [{Who, Balance+X}|T];
deposit(Who, X, [H|T]) ->   
    [H|deposit(Who, X, T)];
deposit(Who, X, []) ->
    [{Who, X}].