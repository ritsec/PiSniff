INSERT_DATA_ENTRY = '''
INSERT INTO {table_name}(timestamp,
                         location_code,
                         mac_address,
                         start_time,
                         end_time,
                         total_time,
                         avg_signal_strength,
                         min_signal_strength,
                         max_signal_strength) 
VALUES(TIMESTAMP '{timestamp}',
       {location_code},
       '{mac_address}',
       TIMESTAMP '{start_time}',
       TIMESTAMP '{end_time}',
       AGE(TIMESTAMP '{end_time}', TIMESTAMP '{start_time}'),
       {avg_signal_strength},
       {min_signal_strength},
       {max_signal_strength});
'''
