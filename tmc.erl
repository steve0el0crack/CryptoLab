-module(tmc).
-export([start/0, server/1]).

start() ->
    register(tmc, spawn(tmc, server, [[]])),
    io:format("TMC started~n").

server(Routes) ->
    receive
        {From_RSU, {aggregated_routes, AggregatedRoutes}} ->
            io:format("Received aggregated routes: ~p~n", [AggregatedRoutes]),
            % Simulate traffic guidance calculation
            Guidance = calculate_guidance(AggregatedRoutes),
            broadcast_guidance(Guidance),
            server([AggregatedRoutes | Routes])
    end.

calculate_guidance(Routes) ->
    % Simulate guidance calculation based on routes
    {guidance, "Reduce speed on segment1 due to high traffic"}.

broadcast_guidance(Guidance) ->
    vehicle ! {tmc, Guidance}.
