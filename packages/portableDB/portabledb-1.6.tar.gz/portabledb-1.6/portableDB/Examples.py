from portableDB import DATABASE

DTB = DATABASE()
DTB.LogType('COLORFUL') #'BASE' - just normal cmd, 'NONE' - no comments when working
DTB.CreateDatabase('Database') #'Database' - name

DTB.WriteDatabase('Database',['String value', 32], 1) #'Database' - name, [] - here should be your values, 1 - index (can be only positive number)

print(DTB.ReadDatabase('Database', 1, 'ALL')) #'Database' - name, 1 - index, 'ALL' - index of array ('ALL' or any index of value in array, this argument can be ignored, in this case it will work like 'ALL' was given)

DTB.RenameDatabase('DB') #'DB' - new name

DTB.DeleteDatabase('Database') #No comments
