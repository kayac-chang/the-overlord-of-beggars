import {
  useReactTable,
  getCoreRowModel,
  getExpandedRowModel,
  flexRender,
  createColumnHelper,
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
import { Toggle } from "~/components/ui/toggle";
import { Store } from "~/models/store";

const helper = createColumnHelper<Store>();

const columns = [
  helper.display({
    id: "expand",
    cell: (props) =>
      props.row.getCanExpand() && (
        <Toggle
          type="submit"
          pressed={props.row.getIsExpanded()}
          onPressedChange={props.row.toggleExpanded}
          name={!props.row.getIsExpanded() ? "stores" : undefined}
          value={props.row.id}
          // @todo: 展開點下去瞬間 icon 要變成 loading
        >
          {props.row.getIsExpanded() ? "👇" : "👉"}
        </Toggle>
      ),
  }),
  helper.accessor("name", { header: "店名" }),
  helper.accessor("address", { header: "地址" }),
  helper.accessor("distance", {
    header: "距離",
    cell: (props) => {
      const value = props.getValue();

      if (!value) return null;

      return Intl.NumberFormat("zh-TW", {
        style: "unit",
        unit: "meter",
        maximumFractionDigits: 0,
      }).format(value);
    },
  }),
];

type Props = ComponentProps<typeof Table> & {
  data: Store[];
  expanded?: Store["id"];
  renderSubComponent?: (data: Store) => ReactNode;
};
function StoreTable({ data, renderSubComponent, expanded, ...props }: Props) {
  const table = useReactTable({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getRowId: (row) => row.id,
    getRowCanExpand: () => true,
    state: {
      expanded: expanded
        ? {
            [expanded]: true,
          }
        : undefined,
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
          <TableRow>
            {row.getVisibleCells().map((cell) => (
              <TableCell key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </TableCell>
            ))}
          </TableRow>

          {renderSubComponent && row.getIsExpanded() && (
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
