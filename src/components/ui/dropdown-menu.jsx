import { forwardRef } from 'react';
import * as Menu from '@radix-ui/react-dropdown-menu';
import { Check } from 'lucide-react';
import { cn } from '../../lib/utils';

export const DropdownMenu = Menu.Root;
export const DropdownMenuTrigger = Menu.Trigger;
export const DropdownMenuRadioGroup = Menu.RadioGroup;
export const DropdownMenuContent = forwardRef(function DropdownMenuContent({ className, sideOffset = 6, ...props }, ref) {
  return <Menu.Portal><Menu.Content ref={ref} sideOffset={sideOffset} className={cn('z-[110] min-w-44 rounded-xl border border-slate-200 bg-white p-1.5 text-sm text-slate-900 shadow-xl dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 motion-safe:data-[state=open]:animate-in motion-safe:data-[state=open]:fade-in-0 motion-safe:data-[state=open]:zoom-in-95', className)} {...props} /></Menu.Portal>;
});
export const DropdownMenuRadioItem = forwardRef(function DropdownMenuRadioItem({ className, children, ...props }, ref) {
  return <Menu.RadioItem ref={ref} className={cn('relative flex min-h-10 cursor-default select-none items-center rounded-lg py-2 pl-8 pr-3 outline-none focus:bg-slate-100 dark:focus:bg-slate-800', className)} {...props}><span className="absolute left-2"><Menu.ItemIndicator><Check size={14} /></Menu.ItemIndicator></span>{children}</Menu.RadioItem>;
});
