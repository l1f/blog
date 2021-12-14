export interface UserData {
    id: number
    email: string
    confirmed: boolean
    member_since: string
    name: string | null
    role_id: number | null
}

export enum DialogTypes {
    primary = "primary",
    secondary = "secondary",
    success = "success",
    danger = "danger",
    warning = "warning",
    info = "info",
    light = "light",
    dark = "dark",
}