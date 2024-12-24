# Auto-generated file for alternativ_recurrence.m
file_content = '''
% Example usage
disp(['T(10) = ', num2str(altrec(10))]);
disp(['T(20) = ', num2str(altrec(20))]);
disp(['T(30) = ', num2str(altrec(30))]);

function T = altrec(n)
    if n == 0
        T = 1;   return;
    elseif n == 1
        T = 2;   return;
    end
    
    % Initialize T(0) and T(1)
    T0 = 1;     T1 = 2;
    for i = 2:n
        T2 = 2*T1 - T0; 
        T0 = T1; 
        T1 = T2; 
    end
    
    T = T1; % Final result for T(n)
end


'''
