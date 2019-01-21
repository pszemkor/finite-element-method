
f =@(x) x;
g1 = 1 ;
u0 = 1;
N = 5;

h = 2/N;
% Punkty siatki
x = 0 : 2/N : 2;
% Wypelniamy macierz ukladu
A = zeros(N);
for k = 1 : N
    % Wype³niam g³ówn¹ przek¹tn¹
    if (k*h == 1)
        A(k, k) = 2/h - 1/2;
    elseif ( ((k*h -h < 1) && (k*h >1)) || ((k*h < 1) && (k*h + h >1)) )
        A(k, k) = 2/h - 1/8;
    else 
        A(k,k) = 2/h;
    end  
    % Wype³niam dwie pozosta³e przek¹tne:
    %dolna przek¹tna
    if (k > 1)
        if (k*h <= 1)
             A(k, k-1) = -1/h -1/2;
        elseif (k*h - h >= 1)
             A(k, k-1) = -1/h -1;
        else 
            A(k, k-1) = -1/h -7/8;
        end 
        %górna przek¹tna
        if((k-1)*h >= 1)
            A(k-1, k) = -1/h +1;
        elseif((k-1)*h + h <= 1)
            A(k-1, k) = -1/h +1/2;
        else
            A(k-1, k) = -1/h + 5/8;
        end 
    end
end
A(N,N) = 1/h + 1;

% metoda Simpsona 
B = zeros(N, 1);
for k = 1 : N
    B(k, 1) = f(h*k) * 4*h/3;
end
% Uwzgledniamy warunki brzegowe Dirichleta
B(1, 1) = B(1, 1) - u0 * (-1/h - 1/2);
B(N,1) = (f(2) + 2 * f(2 - (h / 2))) * h / 6 + g1;
msgbox(num2str(A));
% Rozwiazujemy uklad rownan A * wynik = B
wynik = A \ B;
%msgbox(num2str(B));
% Konstruujemy wektor wartosci u(x) dla wezlow wewnetrznych
u = zeros(1, N+1);
u(2:N+1) = wynik;
% warunek Dirichleta
u(1) = u0;
msgbox(num2str(u));
% Rysujemy wyliczone punkty (funkcja plot dodaje 'wizualna' interpolacje)
plot(x, u);