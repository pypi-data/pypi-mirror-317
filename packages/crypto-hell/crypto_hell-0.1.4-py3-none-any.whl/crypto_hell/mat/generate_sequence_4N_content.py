# Auto-generated file for generate_sequence_4N.m
file_content = '''
% Example usage
generate_sequence(10);
generate_sequence(20);
generate_sequence(30);
generate_sequence(40);

function generate_sequence(N)
    sequence = zeros(1, N);
    for k = 1:N
        sequence(k) = 4 * k + 1;
    end

    % Display the result
    disp(['Sequence for N = ', num2str(N), ':']);
    disp(sequence);
end


'''
