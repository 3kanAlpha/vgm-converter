import yaml
import argparse, os, sys, glob, subprocess

CONFIG_FILE = 'conf.yml'

def check_conf():
    print('Loading configuration...')
    
    if not os.path.exists(CONFIG_FILE):
        print('Configuration file not found. Creating...')
        s = input('Path of test.exe: ')
        data = {'vgmstream': s}
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(data, f)
    
    with open(CONFIG_FILE, 'r') as f:
        conf = yaml.safe_load(f)
    return conf

def convert(args):
    conf = check_conf()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    files = glob.glob(os.path.join(args.input_dir, '*.*'))
    c = len(files)
    
    if c == 0:
        print('Nothing to convert. Exiting...')
        sys.exit(0)
    
    print('{} file(s) found.'.format(c))
    for file in files:
        basename = os.path.basename(file)
        root, ext = os.path.splitext(basename)
        
        print('Converting: {}'.format(basename))
        
        cp = subprocess.run([conf['vgmstream'], '-o', os.path.join(args.output_dir, root + '.' + args.ext), file])
        print()
    
    print('Done.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', help='The directory that contains the audio files.', default='./inputs/')
    parser.add_argument('-o', '--output-dir', help='The directory that will contain the converted files.', default='./outputs/')
    parser.add_argument('-e', '--ext', help='The extension of the converted files.', default='wav')
    args = parser.parse_args()
    convert(args)

if __name__ == '__main__':
    main()
    