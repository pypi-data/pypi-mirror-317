# Auto-generated file for HarmonicSum.m
file_content = '''
% Example usage
harmonic_sum(10);
harmonic_sum(20);
harmonic_sum(30);

function H = harmonic_sum(N)
    H = 0;
    for k = 1:N
        H = H + 1/k; 
    end

    disp(['Harmonic sum for N = ', num2str(N), ': ', num2str(H)]);
end


'''
