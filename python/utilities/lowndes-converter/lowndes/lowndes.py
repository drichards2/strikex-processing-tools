"""Tools to read and write Lowndes files"""

import os.path
import pandas

BELL_IDENTIFIERS = ( '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O', 'E', 'T', 'A', 'B', 'C', 'D' )


def read( infile ):
    """Read a file in Lowndes format.
    Args:
        infile (str): Filename of the Lowndes file to read

    Returns:
        Dictionary with two keys - one key 'info' containing metadata from the file and another
        'strikedata' containing a pandas DataFrame with the strike information"""
    
    strike_count = 0
    base_offset = 0
    last_timestamp = 0

    metadata = {}
    metadata['basename'] = os.path.split(infile)[1]

    strikedata = { 'handstroke': [], 'bell': [], 'time': [] }

    line_count = 1
    
    with open( infile, 'rt') as istrm:
        for line in istrm:
            line = line.strip()
            line_count += 1
            if '#.' in line:
                if 'Lowndes:' in line:
                    metadata['version'] = line[12:]
                elif 'Creator:' in line:
                    metadata['creator'] = line[12:]
                elif 'TranscriptionDate:' in line:
                    metadata['transcription_date'] = line[22:]
                elif 'FirstBlowMs:' in line:
                    metadata['first_blow'] = int(line[16:])
            else:
                blowdata = line.split()
                if len(blowdata) == 3:
                    handstroke = blowdata[0] == 'H'
                    if blowdata[1] not in BELL_IDENTIFIERS:
                        print 'Unrecognised bell identifier {0} at line {1}'.format( blowdata[1], line_count )
                        continue
                    bell = BELL_IDENTIFIERS.index( blowdata[1] ) + 1
                    timestamp = int( blowdata[2], 16)

                    if (timestamp < last_timestamp):
                        base_offset += 65536

                    strike_time = timestamp + base_offset
                    strike_count += 1

                    last_timestamp = timestamp
                    strikedata['handstroke'].append( handstroke )
                    strikedata['bell'].append( bell )
                    strikedata['time'].append( strike_time )


    pandas_frame = pandas.DataFrame( data=strikedata )
    if 'bells' not in metadata:
        metadata['bells'] = pandas_frame['bell'].max()
    return { 'info': metadata, 'strikedata': pandas_frame }

def __bell_to_symbol( bell_number ):
    """Turn a bell number into a alphanumeric symbol representing the bell
    Args:
        bell_number (int): Bell number to convert

    Returns:
        Bell symbol as string"""
    
    if (bell_number <= 0) or (bell_number > len( BELL_IDENTIFIERS ) ):
        raise '{0} is not a valid bell number'.format( bell_number)

    return BELL_IDENTIFIERS[bell_number-1]
    

        
def write( outfile, lowndes_data ):
    """Write a file in Lowndes format.
    Args:
        infile (str): Filename of the Lowndes file to read
        lowndes_data:

        lowndes_data can be in several different formats. The preferred
        is a dictionary containing one key 'info' containing metadata from the file and another
        'strikedata' containing a pandas DataFrame with the strike information"""

    with open(outfile, 'wt') as ostrm:
            if type(lowndes_data)==dict:
                if 'info' in lowndes_data:
                    if 'version' in lowndes_data['info']:
                        print >> ostrm, '#. Lowndes: {0}'.format( lowndes_data['info']['version'] )
                    if 'creator' in lowndes_data['info']:
                        print >> ostrm, '#. Creator: {0}'.format( lowndes_data['info']['creator'] )
                    if 'transcription_date' in lowndes_data['info']:
                        print >> ostrm, '#. TranscriptionDate: {0}'.format( lowndes_data['info']['transcription_date'] )
                    if 'first_blow' in lowndes_data['info']:
                        print >> ostrm, '#. FirstBlowMs: {0}'.format( lowndes_data['info']['first_blow'] )

                if 'strikedata' not in lowndes_data:
                    raise Exception('No strikedata found in lowndes data')

                if type(lowndes_data['strikedata'])==pandas.DataFrame:

                    for strike in lowndes_data['strikedata'].iterrows():
                        panda_frame = strike[1]
                        print >> ostrm, '{0} {1} 0X{2:04x}'.format( 'H' if panda_frame['handstroke'] else 'B', __bell_to_symbol( panda_frame['bell'] ), panda_frame['time'] % 0x10000)
                else:
                    raise Exception('Unrecognised format for strike information in dictionary')

            else:
                raise Exception('Unrecognised format for Lowndes data')
                    
