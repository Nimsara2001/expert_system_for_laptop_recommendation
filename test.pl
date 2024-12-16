laptop('Dell XPS 13', brand('Dell'), processor('Intel i7'), ram(16), storage(512), price(1200), usage('general'), screen('13 inch'), battery('10 hours')).
laptop('HP Spectre x360', brand('HP'), processor('Intel i5'), ram(8), storage(256), price(1000), usage('general'), screen('14 inch'), battery('12 hours')).
laptop('Macbook Pro', brand('Apple'), processor('Intel i5'), ram(8), storage(256), price(1300), usage('general'), screen('13 inch'), battery('10 hours')).

recommend_laptop(Budget, Usage, RAM, Result) :-
    laptop(Result, _, _, ram(R), _, price(P), usage(U), _, _),
    P =< Budget,
    U == Usage,
    R >= RAM.

get_recommendation(Budget, Usage, RAM, Recommendations) :-
    findall(Laptop, recommend_laptop(Budget, Usage, RAM, Laptop), Recommendations).




