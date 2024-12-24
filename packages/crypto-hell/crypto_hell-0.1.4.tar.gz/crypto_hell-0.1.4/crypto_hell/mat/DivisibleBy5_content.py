# Auto-generated file for DivisibleBy5.m
file_content = '''
% Example usage
divisible_by_5(50);
divisible_by_5(100);
divisible_by_5(150);
divisible_by_5(200);

function divisible_by_5(N)
    result = [];
    for i = 1:N
        if mod(i, 5) == 0 
            result = [result, i]; 
        end
    end

    disp(['Numbers divisible by 5 up to N = ', num2str(N), ':']);
    disp(result);
end


'''
