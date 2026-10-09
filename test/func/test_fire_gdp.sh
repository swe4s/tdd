test -e ssshtest || curl -fLsS https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest -o ssshtest

. ./ssshtest

run test_plot_runs python src/plot_fire_gdp.py --out fire_gdp.png
assert_exit_code 0
assert_equal fire_gdp.png "$(ls fire_gdp.png)"