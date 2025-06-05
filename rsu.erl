-module(rsu).
-export([start/0, server/1, request_routes/0]).

start() ->
    register(rsu, spawn(rsu, server, [[]])),
    io:format("RSU started~n").

server(Routes) ->
    receive
        {From_Vehicle, {route, Route}} ->
            NewRoutes = [Route | Routes],
            io:format("Received route from vehicle: ~p~n", [Route]),
            case length(NewRoutes) >= 2 of
                true ->
                    io:format("Aggregating routes and sending to TMC~n"),
                    tmc ! {self(), {aggregated_routes, NewRoutes}};
                false ->
                    ok
            end,
            server(NewRoutes);
        request_routes ->
            vehicle ! {self(), request_route},
            server(Routes)
    end.

request_routes() ->
    rsu ! request_routes.
