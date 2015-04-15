# Author/s: Zach Metcalf
# Test cases for h4A_metcalf847.py
>>> run('125 5 / W')
'25'
>>> run('50 5 | W')
'55'
>>> run('`fail`')
'fail'
>>> run('33 121 117 103 32 121 108 102 32 97 32 115 105 32 114 97 109 108 C 111 86 32 46 114 68 AAAAAAAAAAAAAAAAAAAAAAAAA')
'Dr. Vollmar is a fly guy!'
>>> run('`9 * 9 is `9C*W33A')
'9 * 9 is 81!'
>>> run('`help I am stuck`')
'help I am stuck'
>>> run('55 53 49 52 54 51 56 45 55 49 52 AAAAAAA`-`AAAA')
'417-836-4157'
>>> run('5280 18 % W')
'6'
>>> run('0 Shahahah 42 Pblahblahblah - W')
'42'
>>> run('105 72 AA')
'Hi'
    
