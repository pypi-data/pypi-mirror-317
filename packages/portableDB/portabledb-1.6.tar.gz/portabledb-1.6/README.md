from portableDB import DATABASE

DTB = DATABASE()
DTB.LogState('COLORFUL')
DTB.Create_Database('TXT')

DTB.Write_Database('TXT',['hello worleed', 'loeel', 'poefen', 'poefsdadsen', 'poefasdasfqweren', 'poe42742fen', 'poe42745274862fen', 'poe42742y84fe4564676754n'], 1)

mass = ['1','2','3']
DTB.Write_Database('TXT',mass, 1)

print(DTB.Read_Database('TXT', 1, '2'))

DTB.Rename_Database('TXT','DB')

DTB.Delete_Database('TXT')

