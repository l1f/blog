const deleteButtons: HTMLCollectionOf<Element> | null = document.getElementsByClassName("delete-user")
const dialog = document.getElementById("js-dialog")

interface UserData {
    id: number
    email: string
    confirmed: boolean
    member_since: string
    name: string | null
    role_id: number | null
}

for (const btn of deleteButtons) {
    btn.addEventListener("click", () => {
        confirmDelete(btn.id.replace("user-", ""))
    })
}

const confirmDelete = async (userId: string) => {
    const user = await getUserById(userId)
    clearDialogDiv()
    dialog!.append(deleteDialog(user))
}

const getUserById = async (userId: string): Promise<UserData> => {
    const response = await fetch(`/api/users/${userId}`)
    return await response.json()
}

const clearDialogDiv = () => {
    while (dialog!.firstChild) {
        dialog!.removeChild(dialog!.firstChild)
    }
}

const deleteDialog = (user: UserData): HTMLDivElement => {
    const div = document.createElement("div")
    const btn = document.createElement("button")
    btn.innerText = "yes"
    btn.addEventListener("click", () => {
        console.log(user.id)
    })
    div.className = "alert info"
    div.innerText = `Do you really want to delete ${user.email}?`
    div.append(btn)
    return div
}