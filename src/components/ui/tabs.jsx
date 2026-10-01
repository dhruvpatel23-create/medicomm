import { forwardRef } from 'react';
import * as TabsPrimitive from '@radix-ui/react-tabs';
import { cn } from '../../lib/utils';

export const Tabs = TabsPrimitive.Root;
export const TabsList = forwardRef(function TabsList({ className, ...props }, ref) {
  return <TabsPrimitive.List ref={ref} className={cn('inline-flex items-center gap-5 border-b border-slate-200 dark:border-slate-800', className)} {...props} />;
});
export const TabsTrigger = forwardRef(function TabsTrigger({ className, ...props }, ref) {
  return <TabsPrimitive.Trigger ref={ref} className={cn('relative -mb-px inline-flex min-h-12 items-center justify-center gap-2 border-b-2 border-transparent px-1 text-sm font-medium text-slate-500 transition-colors hover:text-teal-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 data-[state=active]:border-teal-700 data-[state=active]:text-teal-800 dark:text-slate-400 dark:hover:text-teal-200 dark:data-[state=active]:border-teal-300 dark:data-[state=active]:text-teal-200 motion-reduce:transition-none', className)} {...props} />;
});
export const TabsContent = forwardRef(function TabsContent({ className, ...props }, ref) {
  return <TabsPrimitive.Content ref={ref} className={cn('mt-5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500', className)} {...props} />;
});
