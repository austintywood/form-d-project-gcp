{{ config(materialized='table') }}

select      ACCESSIONNUMBER                                 as accession_number
            , INDUSTRYGROUPTYPE                             as industry_group_type
            , INVESTMENTFUNDTYPE                            as investment_fund_type
            , cast(IS40ACT as bool)                         as is_40_act
            , REVENUERANGE                                  as revenue_range
            , AGGREGATENETASSETVALUERANGE                   as aggregate_net_asset_value_range
            , FEDERALEXEMPTIONS_ITEMS_LIST                  as federal_exemptions_items_list
            , cast(ISAMENDMENT as bool)                     as is_amendment
            , PREVIOUSACCESSIONNUMBER                       as previous_accessionnumber
            , cast(SALE_DATE as date)                       as sale_date
            , cast(YETTOOCCUR as bool)                      as yet_to_occur
            , cast(MORETHANONEYEAR as bool)                 as more_than_one_year
            , cast(ISEQUITYTYPE as bool)                    as is_equity_type
            , cast(ISDEBTTYPE as bool)                      as is_debt_type
            , cast(ISOPTIONTOACQUIRETYPE as bool)           as is_option_to_acquire_type
            , cast(ISSECURITYTOBEACQUIREDTYPE as bool)      as is_security_to_be_acquired_type
            , cast(ISPOOLEDINVESTMENTFUNDTYPE as bool)      as is_pooled_investment_fund_type
            , cast(ISTENANTINCOMMONTYPE as bool)            as is_tenant_incommon_type
            , cast(ISMINERALPROPERTYTYPE as bool)           as is_mineral_property_type
            , cast(ISOTHERTYPE as bool)                     as is_other_type
            , DESCRIPTIONOFOTHERTYPE                        as description_of_other_type
            , cast(ISBUSINESSCOMBINATIONTRANS as bool)      as is_business_combination_trans
            , BUSCOMBCLARIFICATIONOFRESP                    as bus_comb_clarification_of_resp
            , cast(MINIMUMINVESTMENTACCEPTED as int64)      as minimum_investment_accepted
            , cast(OVER100RECIPIENTFLAG as bool)            as over_100_recipient_flag
            , TOTALOFFERINGAMOUNT                           as total_offering_amount
            , cast(TOTALAMOUNTSOLD as int64)                as total_amount_sold
            , TOTALREMAINING                                as total_remaining
            , SALESAMTCLARIFICATIONOFRESP                   as sales_amt_clarification_of_resp
            , cast(HASNONACCREDITEDINVESTORS as bool)       as has_non_accredited_investors
            , cast(NUMBERNONACCREDITEDINVESTORS as int64)   as number_non_accredited_investors
            , cast(TOTALNUMBERALREADYINVESTED as int64)     as total_number_already_invested
            , cast(SALESCOMM_DOLLARAMOUNT as int64)         as sales_comm_dollar_amount
            , cast(SALESCOMM_ISESTIMATE as bool)            as sales_comm_is_estimate
            , cast(FINDERSFEE_DOLLARAMOUNT as int64)        as finders_fee_dollar_amount
            , cast(FINDERSFEE_ISESTIMATE as bool)           as finders_fee_is_estimate
            , FINDERFEECLARIFICATIONOFRESP                  as finder_fee_clarification_of_resp
            , cast(GROSSPROCEEDSUSED_DOLLARAMOUNT as int64) as gross_proceeds_used_dollar_amount
            , cast(GROSSPROCEEDSUSED_ISESTIMATE as bool)    as gross_proceeds_used_is_estimate
            , GROSSPROCEEDSUSED_CLAROFRESP                  as gross_proceeds_used_clar_of_resp
            , cast(AUTHORIZEDREPRESENTATIVE as bool)        as authorized_representative
from        {{ source('raw', 'offerings')}}
