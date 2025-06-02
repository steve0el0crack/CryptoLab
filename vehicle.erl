-module(vehicle).
-export([start/0, ask/1, deposit/2, withdraw/2]).

start() ->
    ask({nil, nil}),
    io:format("Hello world'n").

certificate() -> 'bank@super.eua.ericsson.se'.
route() -> {}.
position() -> {1, 2, 3}.

ask(Who) -> call_bank({ask, Who}).
deposit(Who, Amount) -> call_bank({deposit, Who, Amount}).
withdraw(Who, Amount) -> call_bank({withdraw, Who, Amount}).

call_bank(Msg) ->
    Headoffice = head_office(),
    monitor_node(Headoffice, true),
    {bank_server, Headoffice} ! {self(), Msg},
    receive
        {bank_server, Reply} ->
            monitor_node(Headoffice, false),
            Reply;
        {nodedown, Headoffice} ->
            no
    end.