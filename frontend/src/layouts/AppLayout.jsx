import { Outlet } from 'react-router-dom'
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar'
import { TooltipProvider } from '@/components/ui/tooltip'
import AppSidebar from '@/components/AppSidebar'

/* Shell for the signed-in part of the app: everything nested under this
   route gets the sidebar, and nothing else does.

   The sign in guard goes here once /login exists again. */
function AppLayout() {
    return (
        <TooltipProvider>
            <SidebarProvider>
                <AppSidebar />
                <SidebarInset>
                    <header className="flex items-center gap-2 border-b px-4 py-3">
                        <SidebarTrigger />
                    </header>
                    <main className="p-8">
                        <Outlet />
                    </main>
                </SidebarInset>
            </SidebarProvider>
        </TooltipProvider>
    )
}

export default AppLayout
