current_time = Time.now.strftime('%H:%M')
# current_time_h = Time.now.strftime("%H").to_i
# current_time_m = Time.now.strftime("%M").to_i
time = Time.new
current_time_h = time.hour
current_time_m = time.min

print "Your current time is: #{current_time} "

if current_time_h >= 0 && current_time_h <= 6
    puts 'Zzzzzz'
elsif (current_time_h >= 6 && current_time_m != 0) && (current_time_h <= 12)
    puts 'Good Morning'
elsif (current_time_h >= 12 && current_time_m >= 0) && (current_time_h < 18)
    puts 'Good Afternoon'
else
    puts 'Good Evening'
end
