 %MACRO V21H87M1(ICD9=);
 %***********************************************************************
 ************************************************************************

 1  MACRO NAME:      V21H87M1
 2  PURPOSE:         to assign additional CC for some ICD9s
 3  PARAMETERS:      ICD9 - diagnosis variable in a diagnosis file
 ***********************************************************************;
   IF &ICD9 IN ("3572","36202" )
   THEN CC18  = 1 ;
   ELSE
   IF &ICD9 IN ("40401","40403","40411","40413","40491","40493" )
   THEN CC85  = 1 ;

 %MEND V21H87M1;
