import sys
import argparse

parser = argparse.ArgumentParser(
    description='Convert a Flipper .sub file to .csv')
parser.add_argument('-i', '--input', help='Flipper .sub file', required=True)
parser.add_argument('-o', '--output', help='Output .csv file', required=True)
parser.add_argument('--interpolate', help='Interpolate data (vs use original data points)',
                    nargs='?', const=True, required=False)
parser.add_argument('--decimation',  type=int,
                    help='Only use every Nth sample', nargs='?', const="7", required=False)
args = parser.parse_args()


INPUT_FILE = args.input
OUTPUT_FILE = args.output
CONT_DATA = True if args.interpolate is None else args.interpolate      # interpolate original data?
SAMPLE_SIZE = 1         # divide the timestamp data by this value
DECIMATION = 1 if args.decimation is None else args.decimation         # only use every N samples

f = open(INPUT_FILE)
a = f.read()

data = a.split('\n')
samples = []
for d in data:
    if "RAW_Data" in d:
        samples += (d.split(': ')[1].split(' '))

print("Samples on .sub file: ", len(samples))

values = []
t = 0

for s in samples:
    bit_val = 1 if int(s) >= 0 else 0
    if CONT_DATA == False:
        t = t + abs(int(s))/SAMPLE_SIZE
        values.append((t, bit_val))
    else:
        for u in range(abs(int(s))):
            t += 1/SAMPLE_SIZE
            values.append((t, bit_val))

# decimation
dec_val = []
i = 0
for v in values:
    i += 1
    if i % DECIMATION == 0:
        dec_val.append(v)
values = dec_val


if OUTPUT_FILE != None:
    f = open(OUTPUT_FILE, "w")
    f.write("Time[s], Ch1 \n")
    samples = 0
    print("Samples on CSV file:", len(values))
    for v in values:
        f.write("{:.16f}".format(v[0]) + ", " + str(v[1]) + "\n")
        samples += 1
        # if samples >= MAX_SAMPLES: break

    f.close()

print("Done.")
