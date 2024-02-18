{{ config(materialized='table') }}

select      ACCESSIONNUMBER                     as accession_number
            , FILE_NUM                          as file_num
            , case
                when regexp_contains(FILING_DATE, r'[A-Za-z]') then parse_date('%d-%b-%Y', FILING_DATE)
                else cast(FILING_DATE as datetime)
            end                                 as filing_datetime
            , SIC_CODE                          as sic_code
            , SCHEMAVERSION                     as schema_version
            , SUBMISSIONTYPE                    as submission_type
            , TESTORLIVE                        as test_or_live
            , cast(OVER100PERSONSFLAG as bool)  as over_100_persons_flag
            , cast(OVER100ISSUERFLAG as bool)   as over_100_issuer_flag
from        {{ source('raw', 'submissions')}}
