import itertools
import whois

# 生成所有三字母组合
letters = 'abcdefghijklmnopqrstuvwxyz'
three_letter_combinations = [''.join(i) for i in itertools.product(letters, repeat=3)]

# 5jtl.com
# 2345tl.com


#  gogott

available_domains = []

with open('result.txt', 'w') as wf:
    wf.write('f')

for domain in three_letter_combinations:
    try:
        w = whois.whois(f"{domain}.com")
        if not w.domain_name:  # 如果没有找到注册信息，则认为该域名可用
            available_domains.append(f"{domain}.com")
            with open('result.txt', 'w') as wf:
                wf.write(f"{domain}.com")
            print('aaa', f"{domain}.com")
        else:
            print('not ava', f"{domain}.com")
    except Exception as e:
        print(f"Error checking {domain}.com: {e}")

print("Available domains:")
for d in available_domains:
    print(d)