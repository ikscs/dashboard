export const API_BASE_URL_PG = import.meta.env.VITE_API_BASE_URL_PG
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL


export const API_ENDPOINTS = {
    HELLO: `${API_BASE_URL}/api/hello/`,
    CURRENCY_RATES: `${API_BASE_URL}/api/currency-rates/`,
    ADVERTISEMENT: `${API_BASE_URL}/api/stat-group-7d/`,
    V_UTM: `${API_BASE_URL}/api/v-utm/`,
    V_OUR: `${API_BASE_URL_PG}/api_mk/v_our`,
    V_TOPIC: `${API_BASE_URL_PG}/api_mk/v_topic`,
    V_TOP: `${API_BASE_URL_PG}/api_mk/v_top`,
    V_TOP_D: `${API_BASE_URL_PG}/api_mk/v_top_d`,
    META_TAGS: `${API_BASE_URL_PG}/api_mk/meta_tags`,
    META_GROUP_IKSCS: `${API_BASE_URL_PG}/api_cp/v_meta_group_ikscs`,
    META_GROUP_MC: `${API_BASE_URL_PG}/api_cp/v_meta_group_mc`,
    CATEGORIES_IKSCS: `${API_BASE_URL_PG}/api_cp/n9dv8_jshopping_categories`,
    CATEGORIES_MC: `${API_BASE_URL_PG}/api_cp/u8w4d_jshopping_categories`,
    PROJECT_KP: `${API_BASE_URL_PG}/api_redmine/project_kp`,
    PROJECTS_IN_PROGRESS: `${API_BASE_URL_PG}/api_redmine/v_projects`,
    PROJECT_ISSUES: `${API_BASE_URL}/api_redmine/v_projects_issues`,
    GADS_SELECT_QUERY: `${API_BASE_URL_PG}/api_mk/_gads_select_query`,
    HELP: `${API_BASE_URL_PG}/api_dashboard/help`
}

export const API_HEADERS = {
    SEO: {
        'Accept-Profile': 'seo'
    },
    IKSCS: {
        'Accept-Profile': 'ikscs'
    },
    MC: {
        'Accept-Profile': 'mc'
    },
    ADV: {
        'Accept-Profile': 'ads'
    },
    CP: {
        'Accept-Profile': 'cp'
    }
} 