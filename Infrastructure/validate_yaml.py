import sys
import yaml

path = r'c:\Users\p_m_a\Aurora\Portal\Portal\Infrastructure\main.yml'

def main():
    try:
        with open(path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print('YAML parse: OK')
    except Exception as e:
        print('YAML parse: ERROR')
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
