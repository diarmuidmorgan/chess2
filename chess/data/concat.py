f_new=open('allminedgames.csv', 'w')
f_new.write('gameNumber,move,winner,whiteRating,blackRating,opening,victory_type,00,01,02,03,04,05,06,07,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,40,41,42,43,44,45,46,47,50,51,52,53,54,55,56,57,60,61,62,63,64,65,66,67,70,71,72,73,74,75,76,77,moves,captures,protects,forks,basicScore,pins,centrePawns,pawnsGuardingKings,kingMoves,pawnRanks,fianachettos,checked,centrePawns,hasCastled,enpassants,\n')
f_new.close()
for i in range(0,21):

    if i==0:
        t=''
    else:
        t=str(i)

    m=open('minedgames'+t+'.csv','r')
    f=m.read()
    m.close()
    f=f.split('\n')
    f=f[1:]
    if f[-1]=='\n':
        f=f[:-1]
    f_new=open('allminedgames.csv','a')
    for line in f:
        f_new.write(line+'\n')

    f_new.close()
