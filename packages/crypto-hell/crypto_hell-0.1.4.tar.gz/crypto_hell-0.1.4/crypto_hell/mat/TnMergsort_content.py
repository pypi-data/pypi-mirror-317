# Auto-generated file for TnMergsort.m
file_content = '''
% Example usage
T_30 = compute_T(30);
T_50 = compute_T(50);

disp(['T(30) = ', num2str(T_30)]);
disp(['T(50) = ', num2str(T_50)]);

function T = compute_T(n)
    if n == 1
        T = 1; % Base case
    else
        T = 2 * compute_T(n/2) + 3 * n; % Recursive case
    end
end


'''
