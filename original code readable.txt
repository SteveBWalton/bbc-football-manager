This not the actual BBC Basic Code.
But an attempt to make the code readable.

   20   MODE 7
        VDU 23; 8202; 0; 0; 0;
   30   REM ?&220=&00:?&221=&0C:?&20C=&3D:?&20D=&0C
   40   DIM T$(16), PLY%(15), PL$(26), SK%(26), ENG%(26), IT%(26), INJ(2), WK(30), SC%(26, 1), D%(4, 1), TP$(3)
   50   *OPT 1, 1
   70   PROCFOOTBALL
   80   *FX 14, 5
  100   ENVELOPE 1, 10, 0, 0, 0, 10, 10, 10, 63, -10, -10, -10, 126, 100
  110   CUP$ = "1st Round      2nd Round      Quarter Final  Semi Final     FINAL          Champions      "
  120   INPUT '''''"ÜENTER YOUR NAMEÖ"MAN$
  130   PRINT "ÜENTER LEVEL (1-4) ";
  140   L% = GET
        L% = L% - 49
        IF L% < 0 OR L% > 3 THEN
            VDU 7
            GOTO 140
  150   PRINT "Ö";L%+1
  160   PRINT "ÜDO YOU WANT SOUND ?";
  170   IF FNYES THEN
            PRINT "ÖYes"
            S% = -15
        ELSE
            PRINT"ÖNo"
            S% = 0
  180   PRINT "ÜDO YOU WANT TO LOAD A 'GAME'";
  190   IF  FNYES THEN
            PRINT "ÖYes"
            PROCLOAD
            GOTO 450
        ELSE
            PRINT "ÖNo"
  200   *FX 13, 5
  210   PROCPICKTEAM
  320   X% = OPENIN("L.PLAY")
        FOR F% = 1 TO 26
            INPUT #X%, PL$(F%)
            SK%(F%) = RND(5)
            ENG%(F%) = RND(10)+10
            NEXT
        FOR F% = 1 TO 4
            SK%(RND(26)) = 5
            NEXT
        CLOSE #X%
  330   R$ = ""
        E$ = ""
        e$ = ""
        AA% = 0
        CP% = 6
        N% = FALSE
        MON% = 50000
        OWE = 200000
        PK = 0
        IT% = 12
        IJ% = 0
        NJ% = 0
  340   FOR F% = 1 TO 12
  350       REPEAT
                A = RND(26)
                UNTIL IT%(A) <> 1
  360       IT%(A) = 1
  370       NEXT
  380   divison = 4
        T$(7) = STRING$(10, " ") + YT$
        L = 7
        PROCDIVISON
  390   M% = 0
        FOR F = 1 TO 3
            TP$(F) = ""
            NEXT
        match = 0
  400   PROCSORT
  410   F% = 0
        REPEAT
            F% = F%+1
            PROCIN(F%)
            UNTIL PK = 11 OR F% = 26
  420   ML$ = MID$(T$(8), 12)
  430   FOR F = 0 TO 15
            PLY%(F) = 0
            NEXT
        PLY%(L) = 32
  440   FOR F = 0 TO 1
            FOR D = 0 TO 4
                D%(D, F) = 0
                NEXT
            NEXT
  450   REPEAT
  460       PSEL = 0
            PBUY = 0
            CUPB = 0
            rnd = 4000 - RND(8000)
  470       REM *FX 14, 6
  480       REM ON ERROR GOTO 6090
  490       CLS
  500       PRINT "ÉMANAGER:";MAN$
  510       IF N% THEN
                PRINTSPC(8)"Öis the manager of the year"
  520       PRINT "ÉLEVEL ";L%+1
  530       PRINT TAB(5);YT$;"'s titles"
  540       IF (AA% AND 1) THEN
                PRINT TAB(7);"Ö";R$
  550       IF (AA% AND 2) THEN
                PRINT TAB(7);"ÉF.A. Cup"
  560       IF  (AA% AND 4) THEN
                PRINTTAB(7);"ÇLeague Cup"
  570       IF (AA% AND 8) THEN
                PRINTTAB(7);"Ü"e$
  580       *TYPE T.MENU
  650       *FX 15, 1
  660       A = GET
  670       IF A = 49 THEN
                PROCSELL
                GOTO 490
  680       IF A = 50 THEN
                PROCLEND
                GOTO 490
  690       IF A = 51 THEN
                PROCRENAME
                GOTO 490
  700       IF A = 53 THEN
                PROCSAVE
  710       IF A = 54 THEN
                PROCRESTART
  720       IF A = 55 THEN
                PROCLEAGUE
                PROCWAIT
  730       IF A <> 52 THEN
                GOTO 490
  740       match = match+1
  750       IF match MOD 6 = 4 AND (CP% AND 2) THEN
                PROCCUPMATCH("F.A. Cup", 1)
  760       IF match MOD 6 = 2 AND (CP% AND 4) THEN
                PROCCUPMATCH("Littlewoods Cup", 2)
  770       IF match MOD 6 = 0 AND (CP% AND 8) THEN
                PROCCUPMATCH(E$, 3)
  780       IF match = 16 THEN
                FOR F% = 0 TO 15
                    PLY%(F%) = PLY%(F%) AND -64
                    NEXT
                PLY%(L) = PLY%(L) OR 32
  790       CLS
  800       F = 0
  810       REPEAT
  820           REPEAT
  830               P = RND(16) - 1
  840               V% = -((MID$(T$(P), 12) < ML$) EOR (match > 15))
  850               UNTIL (PLY%(P) AND 32) = 0
  860           F = F+1
  870           UNTIL V% = ((match+1) AND 1) OR F > 4
  880       PROCCLEAR
            PLY%(P) = PLY%(P) OR 48
            PLY%(L) = PLY%(L) OR 48
  890       IF V% = 0 THEN
                PLY%(P) = PLY%(P)+72
            ELSE
                PLY%(L) = PLY%(L)+72
  900       CLS
            PROCDISPLAY(L, P)
  910       PRINT TAB(15, VPOS-4);
            IF V% = 0 THEN
                PRINT FNDH("ÇHome")
            ELSE
                PRINTFNDH("ÅAway")
  920       *FX 15, 1
  930       A = GET
  940       IF A = 67 THEN
                PROCPICK
  950       IF A <> 9 THEN
                GOTO 900
  960       PRINT SPC(79)
            VDU 11, 11
  970       PROCPLAYMATCH(L, P, (1-V%)/2, V%/2, V%, TRUE)
  980       T$(L) = FNADD(T$(L), 2, LEGOS-ATGOS)
            T$(P) = FNADD(T$(P), 2, ATGOS-LEGOS)
  990       IF ATGOS = LEGOS THEN
                T$(L) = FNADD(T$(L), 1, 1)
                T$(L) = FNADD(T$(L), 4, 1)
                T$(P) = FNADD(T$(P), 1, 1)
                T$(P) = FNADD(T$(P), 4, 1)
                WK(match) = 64
 1000       IF ATGOS < LEGOS THEN
                T$(L) = FNADD(T$(L), 1, 3)
                T$(L) = FNADD(T$(L), 3, 1)
                T$(P) = FNADD(T$(P), 5, 1)
                WK(match) = 128
 1010       IF ATGOS > LEGOS THEN
                T$(P) = FNADD(T$(P), 1, 3)
                T$(P) = FNADD(T$(P), 3, 1)
                T$(L) = FNADD(T$(L), 5, 1)
                WK(match) = 0
 1020       D%(1-SGN(LEGOS-ATGOS), V%) = D%(1-SGN(LEGOS-ATGOS), V%) + 1
            D%(3, V%) = D%(3, V%) + LEGOS
            D%(4, V%) = D%(4, V%) + ATGOS
 1030       WK(match) = WK(match) + 256 * V%
 1040       PRICE = (1-V%) * ((9000+(15-L-P)*500)*(5-divison)+RND(1000))
            IF ABS(FNV(T$(L), 1) - FNV(T$(A), 1)) < 4 THEN
                PRICE = PRICE + (1-V%) * (5-divison) * 3000
 1050       PROCPLAYERS
            PRINT TAB(0, 23);
            PROCINJ
 1060       PROCWAIT
 1070       PROCREST
            PROCRESET
            PROCSORT
            PROCWAIT
            PROCLEAGUE
            PROCWAIT
            PROCMARKET
            PROCREPORT
            PROCPROGRESS
 1080       UNTIL match = 30
 1090   CLS
        R% = FALSE
        PRINT FNDH("àÅEnd of Season")
 1100   PROCWAIT
 1110   PROCLEAGUE
        PROCWAIT
 1120   AA% = AA% AND NOT(1)
        IF L = 0 THEN
            AA% = AA% OR 1
            R$ = "Barclays League Divison " + STR$(divison)
            PROCCUP(R$, YT$)
            M% = M% + 10 - divison * 2
 1130   PROCFOOTBALL
 1140   *FX 14, 5
 1160   IF divison <> 1 THEN
            PRINT CHR$(141)FNDH("ÇPromotion")
        ELSE
            PRINT FNDH("ÇQualify for Europe")
 1170   FOR F = 0 TO 2
            PRINT TAB(5)MID$(T$(F), 11)
            NEXT
 1180   IF divison <> 4 THEN
            PRINT FNDH("ÅRelegation")
            FOR F = 13 TO 15
                PRINT TAB(5)MID$(T$(F), 11)
                NEXT
 1190   IF divison = 1 AND L = 0 THEN
            CP% = CP% OR 64
 1200   IF divison = 1 AND (L = 1 OR L = 2) THEN
            CP% = CP% OR 16
 1210   PROCDIVISON
 1220   B = -(divison < 3)
 1230   FOR F% = 1 TO 26
            SK%(F%) = RND(5) + B
            IT%(F%) = IT%(F%) AND 1
            ENG%(F%) = RND(20)
            SC%(F%, 0) = 0
            SC%(F%, 1) = 0
            NEXT
        IJ% = 0
        NJ% = 0
 1240   F% = 5 - divison
        M% = M% + (15-L)*F%
        F = (F%*40000) - (F%*(L*2000))
 1250   PRINT '"ÇSeason bonus :`";F
 1260   MON% = MON% + F
 1270   PK = 0
        E$ = ""
 1280   IF CP% AND 16 THEN
            E$ = "U.E.F.A. Cup"
 1290   IF CP% AND 32 THEN
            E$ = "European Cup Winners Cup"
 1300   IF CP% AND 64 THEN
            E$="European Champions Cup"
 1310   CP% = 6 - 8 * (E$ <> "")
 1320   IF E$ <> "" THEN
            PRINT "ÇYou qualify for the"'FNDH(E$)
 1330   N% = FALSE
 1340   PROCWAIT
 1350   *FX 13, 5
 1360   IF M% > 60 THEN
            PRINT"ÇYou are in the Manager of the Year     ÇCompetition"
            FOR F = 1 TO 2000
                NEXT
            IF M% > 70 THEN
                PROCCUP("Manager of the Year", MAN$)
                N% = TRUE
 1370   PRINT '" LEVEL ";L%+1'"ÉENTER NEW LEVEL "
 1380   L% = GET-49
        IF L% < 0 OR L% > 3 THEN
            GOTO 1380
 1390   GOTO 390



 1410   DEFFN@(@%, V)
            LOCAL A$, Q%, P%
 1420       Q% = @% AND 128
            P% = @% AND 64
            @% = &1000000 OR (@% AND &FFFF3F)
 1430       A$ = STR$(V)
            IF Q% THEN
            ELSE
                GOTO 1460
 1440       IF LEN(A$) > 6 THEN
                A$ = LEFT$(A$, LEN(A$)-6) + "," + RIGHT$(A$, 6)
 1450       IF LEN(A$) > 3 THEN
                A$ = LEFT$(A$, LEN(A$)-3) + "," + RIGHT$(A$, 3)
 1460       IF P% AND V > 0 THEN
                A$ = "+" + A$
 1470       @% = @% AND &7F
            IF LEN(A$) > @% THEN
                @% = LEN(A$)
 1480       = STRING$(@%-LEN(A$), " ") + A$



 1490   DEFFNMIN(A, B)
            IF A < B THEN
                = A
            ELSE
                = B



 1500   DEFFNMAX(A, B)
            IF A > B THEN
                = A
            ELSE
                = B



 1510   DEFFNV(A$, C%)
            = ASC(MID$(A$, C%)) - 32



 1520   DEFFNSET(A$, C%, V%)
            =LEFT$(A$, C%-1) + CHR$(32 + FNMIN(223, FNMAX(V%, 0))) + MID$(A$, C%+1)



 1530   DEFFNADD(A$, C%, V%)
            =FNSET(A$, C%, V%+FNV(A$, C%))



 1540   DEFFNYES
            LOCAL A%
 1550       REPEAT
                A% = GET AND -33
                UNTIL A% = 89 OR A% = 78
 1560       IF A% = 89 THEN
                =TRUE
            ELSE
                =FALSE



 1570   DEFFNIF(T$, C%)
            IF C% THEN
                = T$
            ELSE
                = ""



 1580   DEFPROCIN(A%)
 1590       IF IT%(A%) <> 1 THEN
                ENDPROC
 1600       T$(L) = FNADD(T$(L), INT((A%-1)/10)+8, SK%(A%))
            T$(L) = FNADD(T$(L), 6, ENG%(A%))
            IT%(A%) = 3
 1610       PK = PK + 1
 1620       ENDPROC



 1630   DEFPROCDROP(A%)
 1640       IF IT%(A%) <> 3 THEN
                ENDPROC
 1650       T$(L) = FNADD(T$(L), INT((A%-1)/10)+8, -SK%(A%))
            T$(L) = FNADD(T$(L), 6, -ENG%(A%))
            IT%(A%) = 1
 1660       PK = PK-1
 1670       ENDPROC



 1680   DEFPROCPLAYMATCH(L, P, LB, PB, V%, L%)
 1690       Y% = VPOS
            PROCMATCH(L, P, LB, PB)
 1700       HT% = FNNEXTGOAL(HG, 0)
            HG = HG-1
            AT% = FNNEXTGOAL(AG, 0)
            AG = AG-1
            LEGOS = 0
            ATGOS = 0
 1710       IF HT% = AT% THEN
                HT% = HT% + 1
 1720       FOR time = 1 TO 90
                T% = TIME
 1730           IF time = HT% THEN
                    LEGOS = LEGOS+1
                    HT% = FNNEXTGOAL(HG, time)
                    HG = HG-1
                    PRINT TAB(2+V%*21, Y%+2+LEGOS);
                    PROCSCORERS
                    HT% = HT% - (AT% = HT%)
 1740           IF time = AT% THEN
                    ATGOS = ATGOS+1
                    PRINTTAB(23-21*V%, Y%+2+ATGOS);time
                    AT% = FNNEXTGOAL(AG, time)
                    AG = AG-1
                    HT% = HT% - (AT% = HT%)
 1750           PRINT TAB(0, Y%);"TIME ";time
 1760           IF V% = 1 THEN
                    PRINT CHR$141;MID$(T$(P), 11);"á";TAB(18);ATGOS;TAB(20);LEGOS;TAB(22);YT$'CHR$141;MID$(T$(P), 11);"á";TAB(18);ATGOS;TAB(20);LEGOS;TAB(22);YT$
 1770           IF V% = 0 THEN
                    PRINT CHR$141;YT$;"á";TAB(18);LEGOS;TAB(20);ATGOS;TAB(22);MID$(T$(P), 11)'CHR$141;YT$;"á";TAB(18);LEGOS;TAB(20);ATGOS;TAB(22);MID$(T$(P), 11)
 1780           IF time = 45 THEN
                    PRINT TAB(15, Y%);"Half Time"
 1790           IF time = 45 AND L% THEN
                    PROCFIXTURES
                    PRINTTAB(35,Y%);TIME-T%-400
 1800           IF time = 45 THEN
                    REPEAT
                        UNTIL TIME > T%+400
                    PRINT TAB(15, Y%);SPC(10)
 1810           REPEAT
                    UNTIL TIME > T%+15
 1820           NEXT
 1830       ENDPROC



 1840   DEFPROCDISPLAY(L,P)
 1850       PRINT TAB(15-LEN(T$(L))/2)MID$(T$(L), 11)TAB(35-LEN(T$(P))/2)MID$(T$(P), 11)
 1860       IF P <> 16 THEN
                PRINT "POS"TAB(10)FN@(2, L+1)TAB(30)FN@(2, P+1)
 1870       PRINT "ENG"TAB(10)FN@(2, INT(FNV(T$(L), 6)/10))TAB(30)FN@(2, INT(FNV(T$(P), 6)/10))'"MOR"TAB(10)FN@(2, FNV(T$(L), 7))TAB(30)FN@(2, FNV(T$(P),7))'"DEF"TAB(10)FN@(2, FNV(T$(L), 8))TAB(30)FN@(2, FNV(T$(P), 8))

 1880       PRINT "MID"TAB(10)FN@(2, FNV(T$(L), 9))TAB(30)FN@(2, FNV(T$(P), 9))'"ATT"TAB(10)FN@(2, FNV(T$(L), 10))TAB(30)FN@(2, FNV(T$(P), 10))
 1890       PRINT 'FNDH("  ÑùÉPicked:"+FN@(2, PK)+"  Squad:"+FN@(2, IT%)+"  Injured:"+FN@(1, IJ%)+"  ú")'''TAB(4)"ÇùáPressàCâto change team       ú"TAB(5);"Çùá Pressà<TAB>âto continune  ú"
 1900       ENDPROC



 1910   DEFFNDH(A$)
 1920       X%=POS
            Y%=VPOS
 1930       PRINT TAB(X%, Y%+1)CHR$141A$TAB(X%, Y%)CHR$141A$
 1940       =""



 1950   DEFPROCSELL
 1960       CLS
 1970       PROCPTEAM
 1980       PRINT " Enter <RETURN> to return to menu"
 1990       PRINT " Else enter player number to be sold"
 2000       INPUT " >"A
 2010       IF A < 0 OR A > 26 THEN
                GOTO 2000
 2020       IF A = 0 THEN
                ENDPROC
 2030       IF (IT%(A) AND 1) = 0 THEN
                PRINT" On range"
                GOTO 2000
 2040       P = SK%(A) * 5000
 2050       P = (P+rnd) * (5-divison)
 2060       PRINT " You are offered `";P
 2070       PRINT " Do you accept"
 2080       IF FNYES THEN
            ELSE
                ENDPROC
 2090       PROCDROP(A)
 2100       IF IT%(A) AND 4 THEN
                IJ% = IJ% - 1
 2110       IT%(A) = IT%(A) AND 4
            IT% = IT% - 1
            PSEL = PSEL + P
            rnd = 4000-RND(8000)
 2120       ENDPROC



 2130   DEFPROCPTEAM
 2140       PRINT"ÜùÅNAME           SKILL ENERGY PRICE"
 2150       FOR F = 0 TO 26
 2160           IF (IT%(F) AND 1) = 0 THEN
                    GOTO 2240
 2170           IF F < 11 THEN
                    PRINT"ÑùÉ";
 2180           IF F > 10 AND F < 21 THEN
                    PRINT"ÉùÅ";
 2190           IF F > 20 THEN
                    PRINT"áùÖ";
 2200           PRINT PL$(F);"(";F;")";TAB(21);SK%(F);TAB(26);ENG%(F);TAB(30);"`";SK%(F)*5000*(5-divison);
 2210           IF (IT%(F) AND 2) THEN
                    PRINT TAB(37)"ÇP";
 2220           IF (IT%(F) AND 4) THEN
                    PRINT TAB(37)"ÅI";
 2230           PRINT
 2240           NEXT
 2250       ENDPROC



 2260   DEFPROCPICK
 2270       CLS
            PROCPTEAM
 2280       IF PK < 12 THEN
                GOTO 2290
            ELSE
                GOTO 2380
 2290       PRINT "ÇPLAYERS PICKED:";PK
 2300       INPUT" >"A
 2310       IF A < 0 OR A > 26 THEN
                GOTO 2270
 2320       IF A = 0 THEN
                ENDPROC
 2330       IF (IT%(A) AND 1) = 0 THEN
                PRINT " On range"
                GOTO 2300
 2340       IF (IT%(A) AND 2) THEN
                GOTO 2420
 2350       IF (IT%(A) AND 4) THEN
                PRINT"ÅHe is injured"
                GOTO 2300
 2360       PROCIN(A)
 2370       GOTO 2270

 2380       PRINT " Enter player to drop"
 2390       INPUT " >"A
 2400       IF A > 26 OR A < 0 THEN
                GOTO 2390
 2410       IF (IT%(A) AND 2) = 0 THEN
                PRINT " On range"
                GOTO 2390
 2420       PROCDROP(A)
 2430       GOTO 2270



 2440   DEFFNTE(P%)
            LOCAL F%
 2450       F% = -1
            REPEAT
                F% = F%+1
                UNTIL (PLY%(F%) AND 15) = P%
 2460       =F%



 2470   DEFPROCFIXTURES
            LOCAL F%, H%, A%, T%
 2480       FOR F% = 1 TO 7
 2490           REPEAT
                    H% = RND(16)-1
 2500               UNTIL (PLY%(H%) AND 16) = 0
 2510           PLY%(H%) = PLY%(H%) OR (16+F%)
 2520           REPEAT
                    A% = RND(16)-1
 2530               UNTIL (PLY%(A%) AND 16) = 0
 2540           PLY%(A%) = PLY%(A%) OR (16+F%)
 2550           IF PLY%(A%) > PLY%(H%) THEN
                    T% = A%
                    A% = H%
                    H% = T%
 2560           PLY%(A%) = PLY%(A%) OR 8
 2570           NEXT
 2580       FOR F% = 0 TO 6
 2590           T% = F%
 2600           FOR D = F%+1 TO 7
 2610               IF MID$(T$(FNTE(T%)), 12) > MID$(T$(FNTE(D)), 12) THEN
                        T% = D
 2620               NEXT
 2630           PROCC(F%, T%)
 2640           NEXT
 2650       ENDPROC



 2660   DEFPROCC(A%, B%)
            IF A% = B% THEN
                ENDPROC
 2670       LOCAL H1%, H2%, A1%, A2%, PLY%
            H1% = FNTE(A%)
            A1% = FNTE(A%+8)
            H2% = FNTE(B%)
            A2% = FNTE(B%+8)
 2680       PLY%(H1%) = (PLY%(H1%) AND -8) OR B%
            PLY%(A1%) = (PLY%(A1%) AND -8) OR B%
 2690       PLY%(H2%) = (PLY%(H2%) AND -8) OR A%
            PLY%(A2%) = (PLY%(A2%) AND -8) OR A%
 2700       ENDPROC



 2710   DEFPROCREST
            LOCAL F%, H%, A%
 2720       FOR F% = 0 TO 7
 2730           H% = FNTE(F%)
                A% = FNTE(F%+8)
 2740           IF L <> H% AND L <> A% THEN
                    GOTO 2780
 2750           IF L = H% THEN
                    PRINT CHR$141;YT$"á"TAB(18);LEGOS;TAB(20);ATGOS;TAB(22)MID$(T$(P), 11)'CHR$141;YT$"á"TAB(18);LEGOS;TAB(20);ATGOS;TAB(22)MID$(T$(P), 11)
 2760           IF L = A% THEN
                    PRINTCHR$141;MID$(T$(P), 11)"á"TAB(18);ATGOS;TAB(20);LEGOS;TAB(22)YT$'CHR$141;MID$(T$(P), 11)"á"TAB(18);ATGOS;TAB(20);LEGOS;TAB(22)YT$
 2770           GOTO 2850
 2780           PROCMATCH(H%,A%,1/2,0)
 2790           PRINT CHR$141;MID$(T$(H%), 11);"á";TAB(18);HG;TAB(20);AG;TAB(22);MID$(T$(A%), 11)'CHR$141;MID$(T$(H%), 11);"á";TAB(18);HG;TAB(20);AG;TAB(22);MID$(T$(A%), 11)
 2800           IF HG = AG THEN
                    T$(H%) = FNADD(T$(H%), 1, 1)
                    T$(H%) = FNADD(T$(H%), 4, 1)
                    T$(A%) = FNADD(T$(A%), 1, 1)
                    T$(A%) = FNADD(T$(A%), 4, 1)
 2810           IF HG > AG THEN
                    T$(H%) = FNADD(T$(H%), 1, 3)
                    T$(H%) = FNADD(T$(H%), 3, 1)
                    T$(A%) = FNADD(T$(A%), 5, 1)
 2820           IF HG < AG THEN
                    T$(A%) = FNADD(T$(A%), 1, 3)
                    T$(A%) = FNADD(T$(A%), 3, 1)
                    T$(H%) = FNADD(T$(H%), 5, 1)
 2830           T$(H%) = FNADD(T$(H%), 2, HG-AG)
                T$(A%) = FNADD(T$(A%), 2, AG-HG)
 2840           PLY%(A%) = PLY%(A%)+64
 2850           NEXT
 2860       ENDPROC



 2870   DEFPROCCLEAR
            LOCAL F%
 2880       FOR F% = 0 TO 15
 2890           PLY%(F%) = PLY%(F%) AND -32
 2900           NEXT
 2910       ENDPROC



 2920   DEFPROCSORT
            LOCAL F,V%
 2930       F = 0
 2940       REPEAT
 2950           sorted=TRUE
 2960           F = F+1
 2970           FOR D = 1 TO 16-F
 2980               IF LEFT$(T$(D), 5) > LEFT$(T$(D-1), 5) OR (LEFT$(T$(D), 5) = LEFT$(T$(D-1), 5) AND MID$(T$(D), 12) < MID$(T$(D-1), 12)) THEN
                        sorted = FALSE
                        PROCSWAP
 2990               NEXT
 3000           UNTIL sorted
 3010       FOR F = 0 TO 15
 3020           IF YT$ = MID$(T$(F), 11) THEN
                    L = F
 3030           NEXT
 3040       WK(match) = WK(match) + 16-L
 3050       ENDPROC



 3060   DEFPROCLEAGUE
 3070       CLS
 3080       PRINT FNDH("Ç*************ÖDIVISON:"+STR$(divison)+"Ç*************")
 3090       PRINT FNDH("ÑùÉ  TEAM              W  D  L PTS DIF")
 3100       FOR F = 0 TO 15
 3110           IF F = L THEN
                    PRINT "à";
                ELSE
                    PRINT " ";
 3120           PRINT FN@(2, F+1)"Ü";MID$(T$(F), 12)"("(PLY%(F)DIV64)")á"STRING$(22-POS, ".")FN@(3, FNV(T$(F), 3))FN@(3, FNV(T$(F),4))FN@(3, FNV(T$(F), 5))FN@(4, FNV(T$(F),1))FN@(68, FNV(T$(F), 2)-100)
 3130           NEXT
 3140       PRINT 'TAB(5);LEFT$(YT$,1);"Matches played:";match
 3150       PRINT TAB(5);YT$"'s position:";L+1
 3160       ENDPROC



 3170   DEFPROCSWAP
            LOCAL A$, PLY%
 3180       A$ = T$(D)
            PLY% = PLY%(D)
            T$(D) = T$(D-1)
            PLY%(D) = PLY%(D-1)
            T$(D-1) = A$
            PLY%(D-1) = PLY%
 3190       ENDPROC



 3200   DEFPROCRESET
 3210       FOR F = 1 TO 26
 3220           IF (IT%(F) AND 1) = 0 THEN
                    GOTO 3250
 3230           IF (IT%(F) AND 2) THEN
                    ENG%(F) = ENG%(F)-RND(2)
 3240           IF (IT%(F) AND 6) = 0 THEN
                    ENG%(F) = ENG%(F)+9
 3250           IF ENG%(F) > 20 THEN
                    ENG%(F) = 20
 3260           IF ENG%(F) < 1 THEN
                    ENG%(F) = 1
 3270           NEXT
 3280       TENG = 0
            FOR F = 1 TO 26
 3290           IF (IT%(F) AND 2) THEN
                    TENG = TENG + ENG%(F)
 3300           NEXT
 3310       T$(L) = FNSET(T$(L), 6, TENG)
 3320       ENDPROC



 3330   DEFPROCMARKET
 3340       IF IT% >= 18 THEN
                CLS
                PRINT "ÇF.A. rules state that one team may not Çhave more that 18 players. You already Çhave 18 players  therefore you may not Çbuy another."
                PROCWAIT
                ENDPROC
 3350       S = RND(26)
 3360       IF (IT%(S) AND 1) THEN
                GOTO 3350
 3370       CLS
 3380       IF S < 11 THEN
                PRINT FNDH("Defence")'"ÑùÉ";
 3390       IF S > 10 AND S < 21 THEN
                PRINT FNDH("Mid-field")'"ÉùÖ";
 3400       IF S > 20 THEN
                PRINT FNDH("Attack")'"áùÖ";
 3410       PRINTPL$(S);TAB(20);SK%(S);TAB(25);ENG%(S);TAB(30);"`";SK%(S)*5000*(5-divison)
 3420       PRINT " Enter your bid"
 3430       PRINT "ÇYou have `";MON%
 3440       *FX 15, 1
 3450       INPUT " >"D
 3460       IF D = 0 THEN
                ENDPROC
 3470       IF D < SK%(S)*5000*(5-divison)+RND(10000)-5000 OR D > MON% THEN
                PRINT"ÅYou're bid is turned down"
                GOTO 3500
 3480       IT%(S) = IT%(S) OR 1
            PRINT "ÇHe's in your squad"
            PBUY = D
            IT% = IT% + 1
 3490       IF IT%(S) AND 4 THEN
                IJ% = IJ%+1
 3500       PROCWAIT
 3510       ENDPROC



 3520   DEFPROCDIVISON
            LOCAL F%, B%, A$
 3530       IF divison = 1 AND L < 13 THEN
                FOR F% = 13 TO 15
                    T$(F%) = ""
                    NEXT
                GOTO 3620
 3540       IF divison = 4 AND L > 2 THEN
                FOR F% = 0 TO 2
                    T$(F%) = ""
                    NEXT
                GOTO 3620
 3550       IF (L > 2 ) AND (L < 13) THEN
                FOR F% = 0 TO 2
                    T$(F%) = ""
                    T$(F%+13) = ""
                    NEXT
 3560       IF L < 3 THEN
                FOR F% = 3 TO 15
                    T$(F%) = ""
                    NEXT
                divison = divison-1
 3570       IF L > 12 THEN
                FOR F% = 0 TO 12
                    T$(F%) = ""
                    NEXT
                divison = divison+1
 3620       FOR F% = 0 TO 15
 3630           IF T$(F%) <> "" THEN
                    T$(F%) = MID$(T$(F%),11)
 3640           NEXT
 3650       B% = L% + 2 * (5-divison)
            T% = 1
 3660       FOR F% = 0 TO 15
 3670           IF T$(F%) = "" THEN
                    T% = T% + 1
                    T$(F%) = FNGETTEAM(divison-1, T%)
 3680           IF INSTR(A$, MID$(T$(F%), 2)) THEN
                    T% = T% + 1
                    T$(F%) = FNGETTEAM(divison-1, T%)
                    GOTO 3680
 3690           A$ = A$ + MID$(T$(F%), 2)
 3700           IF T$(F%) = YT$ THEN
                    L = F%
                    T$(F%) = STRING$(10, " ")+T$(F%)
                    GOTO 3720
 3710           T$(F%) = FNTEAM(T$(F%), divison, 0)
 3720           T$(F%) = FNSET(T$(F%), 7, 10)
                T$(F%) = FNSET(T$(F%), 2, 100)
 3730           NEXT
 3740       ENDPROC



 3750   DEFFNTEAM(A$, DI%, BS%)
 3760       LOCAL D%, M%, A%, B%, R%, F%
            A$ = STRING$(10, " ") + A$
 3770       D% = 3+RND(2)
            M% = 2+RND(3)
            A% = 11-D%-M%
            B% = 1 - (DI% < 4) - (DI% = 1)
            R% = 4 - (DI% AND 1)
 3790       A$ = FNSET(A$, 6, FNRND(20, 11))
 3800       A$ = FNSET(A$, 7, 9+RND(11))
 3810       A$ = FNSET(A$, 8, D%*B%+FNRND(R%, D%))
 3820       A$ = FNSET(A$, 9, M%*B%+FNRND(R%, M%))
 3830       A$ = FNSET(A$, 10, A%*B%+FNRND(R%, A%))
 3840       =A$



 3850   DEFPROCRENAME
 3860       B% = 1
 3870       CLS
            PRINT 0;"àMore Players"
            FOR F = B% TO B%+12
                PRINT F;" ";PL$(F)
                NEXT
 3880       PRINT "àÇEnter 99 to exit"
 3890       INPUT "Å Enter player number to change ";A
 3900       IF A = 0 THEN
                B% = (B%+13) MOD 26
                GOTO 3870
 3910       IF A = 99 THEN
                ENDPROC
 3920       IF A < B% OR A > B%+13 THEN
                GOTO 3870
 3930       PRINT "ÇYou are renaming :"PL$(A)
 3940       INPUT "ÜEnter new name   :"PL$(A)
 3950       PL$(A) = FNCASE(PL$(A))
 3960       ENDPROC



 3970   DEFPROCREPORT
 3980       CLS
 3990       IF PRICE > 0 THEN
                PRINT "ÇGate";STRING$(22-POS, ".");"`"FN@(137, PRICE)
 4000       IF PSEL > 0 THEN
                PRINT "ÇPlayers Sold"STRING$(22-POS, ".");"`"FN@(137, PSEL)
 4010       IF OWE < 0 THEN
                PRINT "ÇInterest"STRING$(22-POS, ".");"`"FN@(137, INT(-OWE*.005))
 4020       IF CUPB > 0 THEN
                PRINT "ÇCup gate"STRING$(22-POS, ".");"`"FN@(137, CUPB)
 4030       PRINT '"ì,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"'
 4040       PRINT "ÅMoney paid to team"STRING$(22-POS, ".");"`"FN@(137, IT%*500*(5-divison))
 4050       IF PBUY > 0 THEN
                PRINT "ÅPlayers bought"STRING$(22-POS,".");"`"FN@(137, PBUY)
 4060       IF OWE > 0 THEN
                PRINT "ÅInterest"STRING$(22-POS, ".");"`"FN@(137, INT(ABS(OWE*.005)))
 4070       PRINT '"ì,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"'
 4080       P% = PRICE + PSEL - INT(OWE*.005) - IT% * 500 * (5-divison) - PBUY + CUPB
 4090       IF P% < 0 THEN
                PRINT FNDH("ÅLOSS"+STRING$(16, ".")+"`"+FN@(137, -P%))
            ELSE
                PRINT FNDH("ÇPROFIT"+STRING$(14, ".")+"`"+FN@(137, P%))
 4100       PRINT '"ì,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"'
            MON% = MON% + P%
 4110       PRINT "ÇTotal money left"STRING$(22-POS, ".");"`"FN@(137, MON%)
 4120       IF OWE > 0 THEN
                PRINT"ÅMoney owed"STRING$(22-POS, ".")"`"FN@(137, OWE)
            ELSE
                PRINT"ÇMoney in bank"STRING$(22-POS, ".")"`"FN@(137, -OWE)
 4130       IF MON% < 0 THEN
                J% = 10^INT(LOG(-MON%))
                OWE = OWE+J%
                MON% = MON%+J%
                SOUND 0, S%, 3, 0.2
                VDU 11, 11, 13
                GOTO 4110
 4140       IF OWE > 1E6 AND MON% <> 0 THEN
                PRINT "The bank want's some money back"
                A% = -MON%*((OWE-MON%) > 1E6) - (OWE-1E6) * ((OWE-MON%) <= 1E6)
                OWE = OWE-A%
                MON% = MON% - A%
                GOTO 4110
 4150       PROCWAIT
 4160       ENDPROC



 4170   DEFPROCLEND
 4180       CLS
 4190       PRINT TAB(16)FNDH("ÉBank")'
 4200       PRINT "ÇYou have `"FN@(137, MON%)
 4210       IF OWE > 0 THEN
                PRINT "ÅYou owe  `"FN@(137, OWE)
            ELSE
                PRINT "ÇIn Bank  `"FN@(137, -OWE)
 4220       PRINT "ÉDo you want to Deposit or Withdraw(D/W)"
 4230       Q = GET
            IF Q <> 68 AND Q <> 87 THEN
                ENDPROC
 4240       IF Q = 68 THEN
                PRINT FNDH("ÇDeposit")
            ELSE
                PRINT FNDH("ÅWithdraw")
 4250       INPUT '"ÜHow much `"A
            IF Q = 87 THEN
                A = -A
 4260       OWE = OWE - A
            MON% = MON% - A
 4270       IF Q = 87 AND OWE > 1E6 THEN
                PRINT '" You cann't have that much"'
                MON% = MON% - (OWE-1E6)
                OWE = 1E6
 4280       IF MON% < 0 THEN
                OWE = OWE - MON%
                MON% = 0
 4290       PRINT '"ÇYou have `"FN@(137, MON%)
 4300       IF OWE > 0 THEN
                PRINT "ÅYou owe  `"FN@(137, OWE)
            ELSE
                PRINT "ÇIn Bank  `"FN@(137, -OWE)
 4310       PROCWAIT
 4320       ENDPROC



 4330   DEFPROCCUPMATCH(a$, C%)
 4340       x = (match-2) DIV 6
            div = RND(4-x)
 4350       IF div < 1 THEN
                div=1
 4360       D% = div-1
 4400       IF C% = 3 THEN
                div = 1 - (div > 2)
                D% = 4
 4410       T$(16) = FNGETTEAM(D%, RND(16))
 4420       IF T$(16) = YT$ THEN
                GOTO 4410
 4430       IF INSTR(TP$(C%), T$(16)) THEN
                GOTO 4410
 4440       T$(16) = FNTEAM(T$(16), div, 0)
 4460       CLS
 4470       C$ = MID$(CUP$, 1+x*15, 15)
            C$ = LEFT$(C$, INSTR(C$, "  ")-1)
            W% = 16-LEN(a$)/2
            PRINT TAB(W%);FNDH("Ç"+a$)
            PRINT TP$(C%)
            W% = 17-LEN(C$)/2
            PRINT TAB(W%)FNDH("É"+C$)
 4480       PROCDISPLAY(L, 16)
 4490       *FX 15, 1
 4500       A = GET
 4510       IF A = 67 THEN
                PROCPICK
 4520       IF A <> 9 THEN
                GOTO 4460
 4530       CLS
            W% = 17-LEN(a$)/2
            PRINT TAB(W%);FNDH("Ç"+a$)
            W% = 17-LEN(C$)/2
            PRINT TAB(W%)FNDH("É"+C$)
 4540       PROCPLAYMATCH(L, 16, 1/2, 1/2, 0, FALSE)
 4550       PRINT TAB(0, 11)
            PROCPLAYERS
            PROCRESET
            PROCINJ
 4560       IF ATGOS = LEGOS THEN
                PRINT " REPLAY"
                T$(16) = FNADD(T$(16), 6, -16)
                FOR f = 1 TO 2000
                    NEXT
                CLS
                GOTO 4470
 4570       IF ATGOS > LEGOS THEN
                PRINT "ÅYou are out of the "'"Å"a$
                CP% = CP% AND NOT(2^C%)
                AA% = AA% AND NOT(2^C%)
                T$(L) = FNADD(T$(L), 7, -3)
                TP$(C%) = MID$(CUP$, 1+15*x, 14)
 4580       IF ATGOS < LEGOS AND x = 4 THEN
                GOTO 4630
 4590       IF ATGOS < LEGOS THEN
                PRINT "ÇYou are in the ";MID$(CUP$, 1+(x+1)*15, 14)'"Çof the ";a$
                T$(L) = FNADD(T$(L), 7, x+3)
                TP$(C%) = TP$(C%)+MID$(CUP$, 1+15*x, 14)+STR$(LEGOS)+" - "+STR$(ATGOS)+" "+MID$(T$(16),11)+CHR$(10)+CHR$(13)
 4600       PRINT "ÇYou made `";55000-div*5000
            CUPB = 55000-div*5000
 4610       PROCWAIT
 4620       ENDPROC

 4630       IF C% = 3 THEN
                e$ = E$
 4640       AA% = AA% OR (2^C%)
 4650       CUPB = 200000
            M% = M%+10
 4660       IF C% = 1 THEN
                CP% = CP% OR 32
 4670       IF C% = 2 THEN
                CP% = CP% OR 16
 4680       IF C% = 3 AND a$ = "European Champions Cup" THEN
                CP% = CP% OR 64
 4690       IF C% = 3 AND a$ = "European Cup Winners Cup" THEN
                CP% = CP% OR 32
 4700       IF C% = 3 AND a$ = "U.E.F.A. Cup" THEN
                CP% = CP% OR 16
 4710       T$(L) = FNSET(T$(L), 7, 25)
 4720       PROCWAIT
 4730       PROCCUP(a$, YT$)
 4740       ENDPROC



 4750   DEFPROCCUP(A$, B$)
 4760       CLS
 4770       E% = 0.5 + LEN(A$) / 2
            W% = 15 - E%
 4780       PRINT TAB(W%)FNDH("àÉ"+A$)
 4790       PRINT TAB(14);"ÖWON BY"
 4800       E% = 0.5 + LEN(B$)/2
            W% = 15 - E%
 4810       PRINT TAB(W%)FNDH("àÅ"+B$)
 4820       *TYPE "T.CUP"
 4970       RESTORE 5070
            FOR F = 5 TO 15
 4980           PRINT TAB(0, F);"ï"
 4990           PRINT TAB(0, F+1);"í"
 5000           IF S% = 0 THEN
                    FOR t = 1 TO 50
                        NEXT
                    GOTO 5040
 5010           READ P, D
 5020           IF P = 999 THEN
                    G = 0
                ELSE
                    G = 1
 5030           SOUND &0201, G, P, D
                SOUND &0202, G, P, D
                SOUND &0203, G, P, D
 5040           PRINT TAB(0, F);"ó"
 5050           PRINT TAB(0, F+1);"ó"
 5060           NEXT
 5070       DATA 97, 15, 97, 5, 101, 5, 999, 5, 101, 5, 97, 5, 101, 10, 97, 2, 89, 5, 81, 5, 77, 10
 5080       PROCWAIT
 5090       ENDPROC



 5100   DEFPROCINJ
 5110       REPEAT
                I = RND(26)
                UNTIL (IT%(I) AND 4) = 0
 5120       PROCDROP(I)
 5130       IF (IT%(I) AND 1) = 1 THEN
                IJ% = IJ% + 1
                PRINT "Å"PL$(I)" has been injured"
 5140       IT%(I) = (IT%(I) AND 1) OR 4
 5150       NJ% = NJ% + 1
 5160       ENDPROC



 5170   DEFPROCPICKTEAM
 5180       G = 1
            @% = 10
 5190       CLS
 5210       VDU 30
            PRINT 0;"àMore Teams"',1;"àOwn Team"
 5220       FOR F = 2 TO 17
 5230           A$ = FNGETTEAM(G-1, F-1)
 5240           PRINT F;A$;SPC(10)
 5250           NEXT
 5260       PRINT " Enter Team Number"
 5270       INPUT " >"A
 5280       IF A = 0 THEN
                G = 1 + (G AND 3)
                GOTO 5210
 5290       IF A = 1 THEN
                INPUT"Enter team name ";A$
                YT$ = "Ü" + FNCASE(LEFT$(A$, 14))
                GOTO 5330
 5300       IF A < 2 OR A > 17 THEN
                GOTO 5260
 5320       YT$ = FNGETTEAM(G-1, A-1)
 5330       PRINT "ÉYou manage";YT$
 5340       ENDPROC



 5350   DEFFNCASE(A$)
            LOCAL F, B$, A%
 5360       FOR F = 1 TO LEN(A$)
 5370           A% = ASC(MID$(A$, F, 1))
                IF A% = 32 AND NOT(B$ = "" OR RIGHT$(B$, 1) = " ") THEN
                    B$ = B$ + " "
                    GOTO 5400
 5380           A% = A% OR 32
                IF A% < 97 OR A% > 122 THEN
                    GOTO 5400
 5390           IF B$ = "" OR RIGHT$(B$, 1) = " " THEN
                    B$ = B$ + CHR$(A% AND 223)
                ELSE
                    B$ = B$ + CHR$(A%)
 5400           NEXT
 5410       =B$



 5420   DEFPROCSAVE
 5425       PRINT "SAVING"
 5430       VDU 28, 0, 24, 39, 22
            MON% = MON% + PSEL
            PSEL = 0
 5440       X = OPENOUT("S." + MID$(YT$, 2, 10))
 5450       PRINT #X, match, MON%, OWE, PK, L, divison, CP%, IT%, IJ%, NJ%, TP$(1), TP$(2), TP$(3), E$, e$, ML$
 5460       FOR F = 1 TO 26
                PRINT #X, PL$(F), SK%(F), ENG%(F), IT%(F), SC%(F, 0), SC%(F, 1)
                NEXT
 5470       FOR F = 0 TO 15
                PRINT #X, PLY%(F), T$(F)
                NEXT
 5480       PRINT #X, M%, N%, R$, AA%
 5490       PRINT #X, D%(3, 0), D%(4, 0), D%(3, 1), D%(4, 1)
 5500       FOR F = 1 TO 30
                PRINT #X, WK(F)
                NEXT
 5510       CLOSE #X
 5520       VDU 26
            ENDPROC



 5530   DEFPROCLOAD
 5540       *FX 13, 5
 5550       PROCPICKTEAM
 5560       VDU 28, 0, 24, 39, 22
 5570       X = OPENIN("S."+MID$(YT$,2,10))
 5580       INPUT #X, match, MON%, OWE, PK, L, divison, CP%, IT%, IJ%, NJ%, TP$(1), TP$(2), TP$(3), E$, e$, ML$
 5590       FOR F = 1 TO 26
                INPUT #X, PL$(F), SK%(F), ENG%(F), IT%(F), SC%(F, 0), SC%(F, 1)
                NEXT
 5600       FOR F = 0 TO 15
                INPUT #X, PLY%(F), T$(F)
                NEXT
 5610       INPUT #X, M%, N%, R$, AA%
 5620       INPUT #X, D%(3, 0), D%(4, 0), D%(3, 1), D%(4, 1)
 5630       FOR F = 1 TO 30
 5640           INPUT #X, WK(F)
 5650           IF F > match THEN
                    GOTO 5670
 5660           D%(2-(WK(F) AND 255) DIV 64, WK(F) DIV 256) = D%(2-(WK(F) AND 255) DIV 64, WK(F) DIV 256)+1
 5670           NEXT
 5680       CLOSE #X
 5690       YT$ = MID$(T$(L), 11)
 5700       VDU 26
 5710       ENDPROC



 5720   DEFPROCRESTART
 5730       CLS
 5740       PRINT FNDH("ÜAre you sure you want to restart")
 5750       A$ = GET$
 5760       IF A$ = "N" THEN
                ENDPROC
 5770       IF A$ = "Y" THEN
                RUN
 5780       GOTO 5750



 5790   DEFPROCPROGRESS
 5800       CLS
            PRINT FNDH(YT$+"'s Progress in Divison:"+STR$(divison))
 5810       PRINT "F.A. Cup";
            IF (CP% AND 2) THEN
                X = (match+2) DIV 6
                PRINT "ÇIN ";MID$(CUP$, 1+X*15, 15)
            ELSE
                PRINT "ÅOUT in ";TP$(1)
 5820       PRINT"League Cup";:IF(CP% AND 4) THEN
                X = (match+4) DIV 6
                PRINT "ÇIN ";MID$(CUP$,1+X*15,15)
            ELSE
                PRINT"ÅOUT in ";TP$(2)
 5830       IF E$ = "" THEN
                GOTO 5850
 5840       PRINT E$;
            IF( CP% AND 8) THEN
                X = match DIV6
                PRINT "ÇIN ";MID$(CUP$, 1+X*15, 15)
            ELSE
                PRINT "ÅOUT in ";TP$(3)
 5850       PRINT '"   [---Home----]   [---Away----]"
 5860       PRINT "   W  D  L  F  A   W  D  L  F  A  PTS"
 5870       FOR F = 0 TO 1
 5880           PRINT CHR$141;
 5890           FOR V = 0 TO 1
 5900               FOR D = 0 TO 4
 5910                   PRINTFN@(3, D%(D, V));
 5920                   NEXT
 5930               PRINT " ";
 5940               NEXT
 5950           PRINT FN@(4, FNV(T$(L), 1))
 5960           NEXT
 5970       Y% = VPOS+1
 5980       PRINT TAB(0, 24)"ÜPress <SHIFT> for next page"TAB(0 ,23)
 5990       VDU 28, 0, 22, 39,  Y%, 14
 6000       FOR D = 1 TO match
 6010           IF (WK(D) AND 256) = 0 THEN
                    PRINT "ÜHome ";
                ELSE
                    PRINT "ÖAway ";
 6020           IF (WK(D) AND 192) = 0 THEN
                    PRINT "ÅLost ";
 6030           IF (WK(D) AND 192) = 128 THEN
                    PRINT "ÇWon  ";
 6040           IF (WK(D) AND 192) = 64 THEN
                    PRINT "ÉDrawn";
 6050           PRINT "Å";
 6060           FOR F = 1 TO (WK(D)AND63)
 6070               IF F = 4 THEN
                        VDU 8, 132
 6080               IF F = 9 THEN
                        VDU8, 130
 6090               IF F = 14 THEN
                        VDU 8, 131
 6100               IF F = 16 THEN
                        VDU 8, 133
 6110               VDU 157
 6120               NEXT
 6130           VDU156
 6140           PRINT TAB(36, VPOS);17-(WK(D)AND63)
 6150           NEXT
 6160       VDU 15, 26
 6170       *FX 15, 1
 6180       PROCWAIT
 6190       CLS
            A$ = MID$(T$(L), 11, 1)
            A$ = CHR$(ASC(A$)+16)
            PRINT A$"h"STRING$(36, ",")"4"'A$"já   Player       Goals Games  Ratio"A$"5"
            P% = 1
 6200       T% = 1
            FOR F% = 2 TO 26
 6210           IF SC%(F%, 0) > SC%(T%, 0) OR (SC%(F%, 0) = SC%(T%, 0) AND SC%(F%, 1) < SC%(T%,1)) THEN
                    T% = F%
 6220           NEXT
            IF SC%(T%, 0) = 0 THEN
                GOTO 6240
 6230       PRINT A$"já"FN@(2, P%)FNCOL(T%)PL$(T%)"á"STRING$(19-POS, ".")FN@(5, SC%(T%, 0))FN@(5, SC%(T%, 1))FN@(&20208, SC%(T%, 0) / SC%(T%, 1))A$"5"
            SC%(T%, 0) = -SC%(T%, 0)
            P% = P% + 1
            IF P% < 6 THEN
                GOTO 6200
 6240       PRINT A$"j"STRING$(36, ",")"5"'A$"já   Player       Games Goals"TAB(37)A$"5"
            P% = 1
 6250       T% = 1
            FOR F% = 2 TO 26
 6260           IF SC%(F%, 1) > SC%(T%, 1) THEN
                    T% = F%
 6270           NEXT
 6280       PRINT A$"já"FN@(2, P%)FNCOL(T%)PL$(T%)"á"STRING$(19-POS, ".")FN@(5, SC%(T%,1));FN@(5, ABS(SC%(T%, 0)))"  ";
 6290       IF T% < 11 THEN
                PRINT "Def";
            ELSE IF T% < 21 THEN
                PRINT"Mid";
            ELSE
                PRINT"Att";
 6300       PRINT TAB(37)A$"5"
            SC%(T%,1) = -SC%(T%, 1)
            P% = P%+1
            IF P% < 12 THEN
                GOTO 6250
 6310       PRINT A$"j"STRING$(36, ",")"5"
 6320       FOR F = 1 TO 26
                SC%(F, 0) = ABS(SC%(F, 0))
                SC%(F, 1) = ABS(SC%(F, 1))
                NEXT
 6330       IF NJ% < 3 THEN
                GOTO 6390
 6340       FOR F% = 3 TO NJ%
 6350           REPEAT
                    I = RND(26)
                    UNTIL(IT%(I) AND 4) = 4
 6360           IT%(I) = IT%(I) AND 3
                IF IT%(I) = 1 THEN
                    IJ% = IJ% - 1
                    PRINT A$"jÇ"PL$(I)" is fit"TAB(37)A$"5"
 6370           NJ% = NJ% - 1
 6380           NEXT
 6390       PRINT A$"*"STRING$(36, ",")"%"
 6400       PROCWAIT
            ENDPROC



 6410   DEFFNCOL(T%)
 6420       IF IT%(T%) AND 2 THEN
                ="Ç"
 6430       IF IT%(T% )AND 4 THEN
                ="Å"
 6440       ="á"


 6450   DEFPROCWAIT
 6460       VDU 26
 6470       *FX 15, 1
 6480       PRINT TAB(0, 24)"Ñùì,,,,,,,,,,ÉPRESS RETURNì,,,,,,,,,,";
 6490       REPEAT
                UNTIL GET = 13
 6500       CLS
 6510       ENDPROC



 6520   REPORT
        PRINT" at line ";ERL
 6530   FOR Z% = 1 TO 7000
            NEXT
 6540   match = match-1
        GOTO 450


 6550   DEFPROCFOOTBALL
 6560       *TYPE"T.FMAN"
 6630       ENDPROC


 6640   DEFFNRND(X%, N%)
 6650       LOCAL T, F%
 6660       FOR F% = 1 TO N%
 6670           T = T + RND(X%)
 6680           NEXT
 6690       =T



 6700   DEFFNNEXTGOAL(A%, T%)
 6710       IF A% = 0 THEN
                =100
 6720       LOCAL B%, C%
            B% = 90
            FOR F = 1 TO A%
 6730           C% = T% + RND(90-T%)
                IF C% < B% THEN
                    B% = C%
 6740           NEXT
 6750       =B%



 6760   DEFPROCPLAYERS
 6770       FOR F% = 1 TO 26
 6780           IF (IT%(F%) AND 2) THEN
                    SC%(F%, 1) = SC%(F%, 1) + 1
 6790           NEXT
 6800       ENDPROC



 6810   DEFPROCSCORERS
 6820       A = RND(4) + RND(2) + 6
            IF A > 10 THEN
                A = 10
 6830       GOAL = RND(FNV(T$(L), A)) - 1
            F% = 0 - 10*(A = 9) -20 * (A=10)
 6840       IF FNV(T$(L), A) = 0 THEN
                GOTO 6820
 6850       REPEAT
 6860           F% = F% + 1
 6870           IF (IT%(F%) AND 2) = 0 THEN
                    F% = F% + 1
                    GOTO 6870
 6880           GOAL = GOAL - SK%(F%)
 6890           UNTIL GOAL < 1
 6900       PRINT PL$(F%);" ";time
            SC%(F%, 0) = SC%(F%, 0) + 1
 6910       ENDPROC



 6920   DEFPROCMATCH(H, A, B1, B2)
 6930       LOCAL X%, Y%
            HAT = FNV(T$(H), 10)
            HMI = FNV(T$(H), 9)
            HDF = FNV(T$(H), 8)
            AAT = FNV(T$(A), 10)
            AMI = FNV(T$(A), 9)
            ADF = FNV(T$(A), 8)
 6940       HAV = B1 + 4*(HAT/ADF)*(HMI/(HMI+AMI)) + (FNV(T$(H), 7)-10) / 40 - (FNV(T$(A), 6)-100) / 400
 6950       AAV = B2 + 4*(AAT/HDF)*(AMI/(AMI+HMI)) + (FNV(T$(A), 7)-10) / 40 - (FNV(T$(H), 6)-100) / 400
 6960       X% = POS
            Y% = VPOS
            PRINT TAB(0, 24)FN@(&20205, HAV)TAB(30, 24)FN@(&20205, AAV)CHR$13TAB(X%, Y%);
 6970       HG = FNPOIS(HAV, FNRND(1, 2) / 2)
            AG = FNPOIS(AAV, FNRND(1, 2) / 2)
 6980       IF HG = AG THEN
                T$(H) = FNSET(T$(H), 7, 10)
                T$(A) = FNSET(T$(A), 7, 10)
 6990       IF HG > AG THEN
                T$(H) = FNSET(T$(H), 7, FNMAX(FNV(T$(H), 7), 10))
                T$(A) = FNSET(T$(A), 7, FNMIN(FNV(T$(A), 7), 10))
 7000       IF HG < AG THEN
                T$(H) = FNSET(T$(H), 7, FNMIN(FNV(T$(H), 7), 10))
                T$(A) = FNSET(T$(A), 7, FNMAX(FNV(T$(A), 7), 10))
 7010       T$(H) = FNADD(T$(H), 7, HG-AG)
            T$(A) = FNADD(T$(A), 7, AG-HG)
 7020       T$(H) = FNSET(T$(H), 7, FNMIN(FNV(T$(H), 7), 20))
            T$(A) = FNSET(T$(A), 7, FNMIN(FNV(T$(A), 7), 20))
 7030       ENDPROC



 7040   DEFFNPOIS(U, C)
            LOCAL P, T%
 7050       T%=0
            P = EXP(-U)
            IF C < P THEN
                =0
 7060       S = P
            REPEAT
 7070           T% = T% + 1
                P = P * U / T%
                S = S + P
 7080           UNTIL C < S
 7090       =T%



 7100   DEFPROC TEST
 7110       CLEAR
            DIM T$(2)
            PK = 0
            IJ% = 0
            IT% = 0
 7120       T$(1) = "     Ñ*882ÉTEAM ONE"
            T$(2) = "     Ñ*882ÉTEAM TWO"
 7130       CLS
            PROCDISPLAY(1, 2)
 7140       PROCMATCH(1, 2, 0, 0)
 7150       INPUT '"TEAM ONE ",MR,EN,DE,MI,AT
            T$(1) = "     " + CHR$(32+MR*10) + CHR$(32+EN) + CHR$(32+DE) + CHR$(32+MI) + CHR$(32+AT) + "ÉTEAM ONE"
 7160       INPUT "TEAM TWO ", MR, EN, DE, MI, AT
            T$(2) = "     " + CHR$(32+MR*10) + CHR$(32+EN) + CHR$(32+DE) + CHR$(32+MI) + CHR$(32+AT) + "ÉTEAM TWO"
 7170       GOTO 7130



 7180   DEFFN GETTEAM(D%, T%)
 7190       LOCAL F%, X%, A$
 7200       X% = OPENIN("L.TEAMS")
 7210       FOR F% = 1 TO T%+D%*16
                INPUT #X%, A$
                NEXT
 7220       CLOSE #X%
 7230       = A$
