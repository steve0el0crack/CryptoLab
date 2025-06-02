-module(rsu).
-export([start/0, server/1]).
start() ->
    register(rsu, spawn(rsu, server, [[]])),
    io:format("Hello world'n").

server(routes) ->
    receive
    {From_Vehicle, {route}} ->
        From_Vehicle ! {rsu, ok},
        routes ++ [route],
        io:format(route),
    case length(routes) of 
        2 ->
            tmc ! {routes};
        _ ->
            server(routes)
    end
end.

%
%lookup(Who, [{Who, Value}|_]) -> Value;
%lookup(Who, [_|T]) -> lookup(Who, T);
%lookup(_, _) -> undefined.
%
%deposit(Who, X, [{Who, Balance}|T]) ->
%    [{Who, Balance+X}|T];
%deposit(Who, X, [H|T]) ->   
%    [H|deposit(Who, X, T)];
%deposit(Who, X, []) ->
%    [{Who, X}].
