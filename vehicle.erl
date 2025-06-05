-module(vehicle).
-export([start/0, server/0, report_route/1]).

start() ->
    register(vehicle, spawn(vehicle, server, [])),
    io:format("Vehicle started~n").

server() ->
    receive
        {From_RSU, request_route} ->
            % Simulate route reporting
            Route = generate_route(),
            From_RSU ! {self(), {route, Route}},
            server();
        {From_TMC, guidance} ->
            io:format("Received guidance: ~p~n", [guidance]),
            server()
    end.

report_route(Route) ->
    rsu ! {self(), {route, Route}}.

generate_route() ->
    % Simulate route generation with segments
    [{segment1, 1}, {segment2, 0}, {segment3, 1}].
