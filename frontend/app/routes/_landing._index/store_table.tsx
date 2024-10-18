import {
  useReactTable,
  getCoreRowModel,
  getExpandedRowModel,
  flexRender,
  ColumnDef,
} from "@tanstack/react-table";
import { ComponentProps, Fragment, ReactNode } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "~/components/ui/table";
import { StoreWithNearExpiredFood } from "~/models/store_with_near_expired_foods";

const columns: ColumnDef<StoreWithNearExpiredFood>[] = [
  {
    id: "expand",
    cell: (props) =>
      props.row.getCanExpand() && (
        <span>{props.row.getIsExpanded() ? "👇" : "👉"}</span>
      ),
  },
  {
    accessorKey: "name",
    header: "店名",
  },
  {
    accessorKey: "address",
    header: "地址",
  },
  {
    accessorKey: "distance",
    header: "距離",
  },
];

type Props = ComponentProps<typeof Table> & {
  data: StoreWithNearExpiredFood[];
  renderSubComponent?: (data: StoreWithNearExpiredFood) => ReactNode;
};
function StoreTable({ data, renderSubComponent, ...props }: Props) {
  const table = useReactTable({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getRowId: (row) => row.id,
    getRowCanExpand: (row) => row.original.nearExpiredFoods.length > 0,
    initialState: {
      columnVisibility: {
        expand: Boolean(renderSubComponent),
      },
    },
  });

  const head = (
    <TableHeader>
      {table.getHeaderGroups().map((headerGroup) => (
        <TableRow key={headerGroup.id}>
          {headerGroup.headers.map((header) => (
            <TableHead key={header.id} colSpan={header.colSpan}>
              {!header.isPlaceholder &&
                flexRender(header.column.columnDef.header, header.getContext())}
            </TableHead>
          ))}
        </TableRow>
      ))}
    </TableHeader>
  );

  const body = (
    <TableBody>
      {table.getRowModel().rows.map((row) => (
        <Fragment key={row.id}>
          <TableRow
            onClick={
              row.getCanExpand() ? row.getToggleExpandedHandler() : undefined
            }
          >
            {row.getVisibleCells().map((cell) => (
              <TableCell key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </TableCell>
            ))}
          </TableRow>

          {row.getIsExpanded() && (
            <TableRow>
              <TableCell colSpan={row.getVisibleCells().length}>
                {renderSubComponent?.(row.original)}
              </TableCell>
            </TableRow>
          )}
        </Fragment>
      ))}
    </TableBody>
  );

  return (
    <Table {...props}>
      {head}
      {body}
    </Table>
  );
}

export default StoreTable;
