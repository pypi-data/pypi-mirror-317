

const unsigned char sqlite3UpperToLower[] = {
      0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,
     18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
     36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
     54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 97, 98, 99,100,101,102,103,
    104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,
    122, 91, 92, 93, 94, 95, 96, 97, 98, 99,100,101,102,103,104,105,106,107,
    108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,
    126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,
    144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,
    162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,
    180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,
    198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,
    216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,
    234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,
    252,253,254,255,
/* NE  EQ  GT  LE  LT  GE  */
   1,  0,  0,  1,  1,  0,  /* aLTb[]: Use when compare(A,B) less than zero */
   0,  1,  0,  1,  0,  1,  /* aEQb[]: Use when compare(A,B) equals zero */
   1,  0,  1,  0,  0,  1   /* aGTb[]: Use when compare(A,B) greater than zero*/
};


#define UpperToLower sqlite3UpperToLower




/*
** 2001 September 15
**
** The author disclaims copyright to this source code.  In place of
** a legal notice, here is a blessing:
**
**    May you do good and not evil.
**    May you find forgiveness for yourself and forgive others.
**    May you share freely, never taking more than you give.
**
*************************************************************************
** An tokenizer for SQL
**
** This file contains C code that implements the sqlite3_complete() API.
** This code used to be part of the tokenizer.c source file.  But by
** separating it out, the code will be automatically omitted from
** static links that do not use it.
*/
// #include "sqliteInt.h"
#ifndef SQLITE_OMIT_COMPLETE
const unsigned char sqlite3CtypeMap[256] = {
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  /* 00..07    ........ */
  0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00,  /* 08..0f    ........ */
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  /* 10..17    ........ */
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  /* 18..1f    ........ */
  0x01, 0x00, 0x80, 0x00, 0x40, 0x00, 0x00, 0x80,  /* 20..27     !"#$%&' */
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  /* 28..2f    ()*+,-./ */
  0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c,  /* 30..37    01234567 */
  0x0c, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  /* 38..3f    89:;<=>? */

  0x00, 0x0a, 0x0a, 0x0a, 0x0a, 0x0a, 0x0a, 0x02,  /* 40..47    @ABCDEFG */
  0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,  /* 48..4f    HIJKLMNO */
  0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,  /* 50..57    PQRSTUVW */
  0x02, 0x02, 0x02, 0x80, 0x00, 0x00, 0x00, 0x40,  /* 58..5f    XYZ[\]^_ */
  0x80, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x22,  /* 60..67    `abcdefg */
  0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,  /* 68..6f    hijklmno */
  0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,  /* 70..77    pqrstuvw */
  0x22, 0x22, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00,  /* 78..7f    xyz{|}~. */

  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* 80..87    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* 88..8f    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* 90..97    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* 98..9f    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* a0..a7    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* a8..af    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* b0..b7    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* b8..bf    ........ */

  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* c0..c7    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* c8..cf    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* d0..d7    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* d8..df    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* e0..e7    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* e8..ef    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,  /* f0..f7    ........ */
  0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40   /* f8..ff    ........ */
};
/*
** This is defined in tokenize.c.  We just have to import the definition.
*/
#define IdChar(C)  ((sqlite3CtypeMap[(unsigned char)C]&0x46)!=0)

int sqlite3_strnicmp(const char *zLeft, const char *zRight, int N){
  unsigned char *a, *b;
  if( zLeft==0 ){
    return zRight ? -1 : 0;
  }else if( zRight==0 ){
    return 1;
  }
  a = (unsigned char *)zLeft;
  b = (unsigned char *)zRight;
  while( N-- > 0 && *a!=0 && UpperToLower[*a]==UpperToLower[*b]){ a++; b++; }
  return N<0 ? 0 : UpperToLower[*a] - UpperToLower[*b];
}

#define sqlite3StrNICmp sqlite3_strnicmp





/*
** Token types used by the sqlite3_complete() routine.  See the header
** comments on that procedure for additional information.
*/
#define tkSEMI    0
#define tkWS      1
#define tkOTHER   2
#ifndef SQLITE_OMIT_TRIGGER
#define tkEXPLAIN 3
#define tkCREATE  4
#define tkTEMP    5
#define tkTRIGGER 6
#define tkEND     7
#endif

typedef unsigned char u8;






#include <vector>









/*
** Return TRUE if the given SQL string ends in a semicolon.
**
** Special handling is require for CREATE TRIGGER statements.
** Whenever the CREATE TRIGGER keywords are seen, the statement
** must end with ";END;".
**
** This implementation uses a state machine with 8 states:
**
**   (0) INVALID   We have not yet seen a non-whitespace character.
**
**   (1) START     At the beginning or end of an SQL statement.  This routine
**                 returns 1 if it ends in the START state and 0 if it ends
**                 in any other state.
**
**   (2) NORMAL    We are in the middle of statement which ends with a single
**                 semicolon.
**
**   (3) EXPLAIN   The keyword EXPLAIN has been seen at the beginning of 
**                 a statement.
**
**   (4) CREATE    The keyword CREATE has been seen at the beginning of a
**                 statement, possibly preceded by EXPLAIN and/or followed by
**                 TEMP or TEMPORARY
**
**   (5) TRIGGER   We are in the middle of a trigger definition that must be
**                 ended by a semicolon, the keyword END, and another semicolon.
**
**   (6) SEMI      We've seen the first semicolon in the ";END;" that occurs at
**                 the end of a trigger definition.
**
**   (7) END       We've seen the ";END" of the ";END;" that occurs at the end
**                 of a trigger definition.
**
** Transitions between states above are determined by tokens extracted
** from the input.  The following tokens are significant:
**
**   (0) tkSEMI      A semicolon.
**   (1) tkWS        Whitespace.
**   (2) tkOTHER     Any other SQL token.
**   (3) tkEXPLAIN   The "explain" keyword.
**   (4) tkCREATE    The "create" keyword.
**   (5) tkTEMP      The "temp" or "temporary" keyword.
**   (6) tkTRIGGER   The "trigger" keyword.
**   (7) tkEND       The "end" keyword.
**
** Whitespace never causes a state transition and is always ignored.
** This means that a SQL string of all whitespace is invalid.
**
** If we compile with SQLITE_OMIT_TRIGGER, all of the computation needed
** to recognize the end of a trigger can be omitted.  All we have to do
** is look for a semicolon that is not part of an string or comment.
*/
extern "C" {


#ifdef __linux__
#define __declspec(v)
#endif



  
  // int sqlite3_complete(const char *zSql){
  __declspec (dllexport) void *sqlite3_complete(const char *zSql) {
    u8 state = 0;   /* Current state, using numbers defined in header comment */
    u8 token;       /* Value of the next token */
    const char* zSqlStart = zSql;
    std::vector <long> *ret = new std::vector <long>;

    /* A complex statement machine used to detect the end of a CREATE TRIGGER
    ** statement.  This is the normal case.
    */
    static const u8 trans[8][8] = {
                      /* Token:                                                */
      /* State:       **  SEMI  WS  OTHER  EXPLAIN  CREATE  TEMP  TRIGGER  END */
      /* 0 INVALID: */ {    1,  0,     2,       3,      4,    2,       2,   2, },
      /* 1   START: */ {    1,  1,     2,       3,      4,    2,       2,   2, },
      /* 2  NORMAL: */ {    1,  2,     2,       2,      2,    2,       2,   2, },
      /* 3 EXPLAIN: */ {    1,  3,     3,       2,      4,    2,       2,   2, },
      /* 4  CREATE: */ {    1,  4,     2,       2,      2,    4,       5,   2, },
      /* 5 TRIGGER: */ {    6,  5,     5,       5,      5,    5,       5,   5, },
      /* 6    SEMI: */ {    6,  6,     5,       5,      5,    5,       5,   7, },
      /* 7     END: */ {    1,  7,     5,       5,      5,    5,       5,   5, },
    };

    while( *zSql ){
      switch( *zSql ){
        case ';': {  /* A semicolon */
          token = tkSEMI;
          break;
        }
        case ' ':
        case '\r':
        case '\t':
        case '\n':
        case '\f': {  /* White space is ignored */
          token = tkWS;
          break;
        }
        case '/': {   /* C-style comments */
          if( zSql[1]!='*' ){
            token = tkOTHER;
            break;
          }
          zSql += 2;
          while( zSql[0] && (zSql[0]!='*' || zSql[1]!='/') ){ zSql++; }
          // if( zSql[0]==0 ) return 0;
          if( zSql[0]==0 ) {
            ret->push_back(-1);
            return ret;
          }
          zSql++;
          token = tkWS;
          break;
        }
        case '-': {   /* SQL-style comments from "--" to end of line */
          if( zSql[1]!='-' ){
            token = tkOTHER;
            break;
          }
          while( *zSql && *zSql!='\n' ){ zSql++; }
          // if( *zSql==0 ) return state==1;
          if( *zSql==0 ) {
            ret->push_back(-1);
            return ret;
          }
          token = tkWS;
          break;
        }
        case '[': {   /* Microsoft-style identifiers in [...] */
          zSql++;
          while( *zSql && *zSql!=']' ){ zSql++; }
          // if( *zSql==0 ) return 0;
          if( *zSql==0 ) {
            ret->push_back(-1);
            return ret;
          }
          token = tkOTHER;
          break;
        }
        case '`':     /* Grave-accent quoted symbols used by MySQL */
        case '"':     /* single- and double-quoted strings */
        case '\'': {
          int c = *zSql;
          zSql++;
          while( *zSql && *zSql!=c ){ zSql++; }
          // if( *zSql==0 ) return 0;
          if( *zSql==0 ) {
            ret->push_back(-1);
            return ret;
          }
          token = tkOTHER;
          break;
        }
        default: {
  #ifdef SQLITE_EBCDIC
          unsigned char c;
  #endif
          if( IdChar((u8)*zSql) ){
            /* Keywords and unquoted identifiers */
            int nId;
            for(nId=1; IdChar(zSql[nId]); nId++){}
  #ifdef SQLITE_OMIT_TRIGGER
            token = tkOTHER;
  #else
            switch( *zSql ){
              case 'c': case 'C': {
                if( nId==6 && sqlite3StrNICmp(zSql, "create", 6)==0 ){
                  token = tkCREATE;
                }else{
                  token = tkOTHER;
                }
                break;
              }
              case 't': case 'T': {
                if( nId==7 && sqlite3StrNICmp(zSql, "trigger", 7)==0 ){
                  token = tkTRIGGER;
                }else if( nId==4 && sqlite3StrNICmp(zSql, "temp", 4)==0 ){
                  token = tkTEMP;
                }else if( nId==9 && sqlite3StrNICmp(zSql, "temporary", 9)==0 ){
                  token = tkTEMP;
                }else{
                  token = tkOTHER;
                }
                break;
              }
              case 'e':  case 'E': {
                if( nId==3 && sqlite3StrNICmp(zSql, "end", 3)==0 ){
                  token = tkEND;
                }else
  #ifndef SQLITE_OMIT_EXPLAIN
                if( nId==7 && sqlite3StrNICmp(zSql, "explain", 7)==0 ){
                  token = tkEXPLAIN;
                }else
  #endif
                {
                  token = tkOTHER;
                }
                break;
              }
              default: {
                token = tkOTHER;
                break;
              }
            }
  #endif /* SQLITE_OMIT_TRIGGER */
            zSql += nId-1;
          }else{
            /* Operators and special symbols */
            token = tkOTHER;
          }
          break;
        }
      }
      state = trans[state][token];
      if (state == 1 && token == tkSEMI) {
        ret->push_back(zSql - zSqlStart);
      }
      zSql++;
    }
    // return state==1;
    ret->push_back(-1);
    return static_cast<void*>(ret);
  }

  __declspec (dllexport) long *getContiguousArray(void *v) {
    return static_cast<std::vector <long> *> (v)->data();
  }

  __declspec (dllexport) void free_complete_list(void *completeList) {
    delete static_cast<std::vector <long> *> (completeList);
  }

}

#endif /* SQLITE_OMIT_COMPLETE */
