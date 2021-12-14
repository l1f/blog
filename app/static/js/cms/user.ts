const deleteButtons: HTMLCollectionOf<Element> | null = document.getElementsByClassName("delete-user")
const dialogDiv = document.getElementById("js-dialog")

interface UserData {
    id: number
    email: string
    confirmed: boolean
    member_since: string
    name: string | null
    role_id: number | null
}

enum DialogTypes {
    primary = "primary",
    secondary = "secondary",
    success = "success",
    danger = "danger",
    warning = "warning",
    info = "info",
    light = "light",
    dark = "dark",
}

type dialogEvent = () => HTMLDivElement;

for (const btn of deleteButtons) {
    btn.addEventListener("click", () => {
        confirmDelete(btn.id.replace("user-", ""))
    })
}

const updateDialog = (event: dialogEvent) => {
    clearDialogDiv()
    dialogDiv!.append(event())
}

const confirmDelete = async (userId: string) => {
    const user = await getUserById(userId)
    updateDialog(() => deleteDialog(user))
}

const getUserById = async (userId: string): Promise<UserData> => {
    const response = await fetch(`/api/users/${userId}`)
    return await response.json()
}

const clearDialogDiv = () => {
    while (dialogDiv!.firstChild) {
        dialogDiv!.removeChild(dialogDiv!.firstChild)
    }
}

const deleteConfirmBtn = (userId: number): HTMLButtonElement => {
    const btn = document.createElement("button")
    btn.innerText = "yes"
    btn.addEventListener("click", async () => {
        console.log(userId)
        const response = await deleteUser(userId)
        if (!response?.ok) {
            updateDialog(() => errorDialog("Error while delete user.. "))
        }
    })

    return btn
}

const dialog = (dialogType: DialogTypes, innerDiv: HTMLDivElement): HTMLDivElement => {
    const div = document.createElement("div")
    div.className = `alert ${dialogType}`
    div.append(innerDiv)

    return div
}

const deleteDialog = (user: UserData): HTMLDivElement => {
    const btn = deleteConfirmBtn(user.id)
    const innerDiv = document.createElement("div")
    innerDiv.innerText = `Do you really want to delete ${user.email}?`
    innerDiv.append(btn)
    return dialog(DialogTypes.danger, innerDiv)
}

const errorDialog = (message: string) => {
    const div = document.createElement("div")
    div.innerText = message

    return dialog(DialogTypes.danger, div)
}

const deleteUser = async (userId: number) => {
    try {
        return await fetch(`/api/users/${userId}`, {
            method: "DELETE"
        })
    } catch (error) {
        updateDialog(() => errorDialog(error.toString()))
    }

}